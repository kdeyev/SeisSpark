from typing import Optional, cast

import pydantic
import pyspark

from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_data.su_pipe import su_process_pipe
from su_rdd.kv_operations import gather_from_rdd_key_value, rdd_key_value_from_gather
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUimp2dParams(pydantic.BaseModel):
    nshot: int = 1
    nrec: int = 1


class SUimp2d(BaseModule):
    def __init__(self) -> None:
        super().__init__(SUimp2dParams, SUimp2dParams())

    @property
    def suimp2d_params(self) -> SUimp2dParams:
        return cast(SUimp2dParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if input_rdd:
            raise Exception("input RDD is not used")
        gather_count_to_produce = self.suimp2d_params.nshot
        trace_count_per_gather = self.suimp2d_params.nrec

        buffers = su_process_pipe(["suimp2d", f"nshot={gather_count_to_produce}", f"nrec={trace_count_per_gather}"], [])
        input_gather = gather_from_rdd_key_value((None, buffers))

        header_entries = input_gather.get_header_entry_values(SEGY_TRACE_HEADER_ENTRIES[SEGYTraceHeaderEntryName.FieldRecord])
        expected = []
        for gather_num in range(1, gather_count_to_produce + 1):
            expected += [gather_num] * trace_count_per_gather
        assert header_entries == expected

        # Create an RDD from in memory buffers
        rdd = suspark_context.context.parallelize([rdd_key_value_from_gather(input_gather)])
        return rdd
