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
from su_rdd.kv_operations import GatherTuple
from su_rdd.rdd_operations import select_by_trace_header


class SelectTracesParams(pydantic.BaseModel):
    key: SEGYTraceHeaderEntryName = SEGYTraceHeaderEntryName.TraceIdenitifactionCode
    value: int = 1


class SelectTraces(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SelectTracesParams, params=SelectTracesParams())

    @property
    def select_traces_params(self) -> SelectTracesParams:
        return cast(SelectTracesParams, self.parameters)

    def _init_rdd(self, seisspark_context: SeisSparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        if not input_rdd:
            raise Exception("input RDD should be specified")
        key: SEGYTraceHeaderEntryName = self.select_traces_params.key
        value: int = self.select_traces_params.value

        rdd = select_by_trace_header(input_rdd, SEGY_TRACE_HEADER_ENTRIES[key], value)
        return rdd
