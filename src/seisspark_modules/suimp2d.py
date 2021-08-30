# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from typing import Optional, cast

import pydantic
import pyspark

from seisspark.seisspark_context import SeisSparkContext
from seisspark.seisspark_module import BaseModule
from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_data.su_pipe import su_process_pipe
from su_rdd.kv_operations import GatherTuple, gather_from_rdd_gather_tuple, rdd_gather_tuple_from_gather


class SUimp2dParams(pydantic.BaseModel):
    nshot: int = 1
    nrec: int = 1


class SUimp2d(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SUimp2dParams, params=SUimp2dParams())

    @property
    def suimp2d_params(self) -> SUimp2dParams:
        return cast(SUimp2dParams, self.parameters)

    def _init_rdd(self, seisspark_context: SeisSparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        if input_rdd:
            raise Exception("input RDD is not used")
        gather_count_to_produce = self.suimp2d_params.nshot
        trace_count_per_gather = self.suimp2d_params.nrec

        buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
        input_gather = gather_from_rdd_gather_tuple((0, buffers))

        header_entries = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
        expected = []
        for gather_num in range(1, gather_count_to_produce + 1):
            expected += [gather_num] * trace_count_per_gather
        assert header_entries == expected

        # Create an RDD from in memory buffers
        rdd = seisspark_context.context.parallelize([rdd_gather_tuple_from_gather(input_gather)])
        # rdd = rdd.mapValues(list)
        return rdd
