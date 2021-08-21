from typing import Optional, cast

import pydantic
import pyspark

from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_rdd.rdd_operations import group_by_trace_header
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUsortParams(pydantic.BaseModel):
    key: SEGYTraceHeaderEntryName = SEGYTraceHeaderEntryName.FieldRecord


class SUsort(BaseModule):
    def __init__(self) -> None:
        super().__init__(SUsortParams, SUsortParams())

    @property
    def susort_params(self) -> SUsortParams:
        return cast(SUsortParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")
        key: SEGYTraceHeaderEntryName = self.susort_params.key

        rdd = group_by_trace_header(input_rdd, SEGY_TRACE_HEADER_ENTRIES[key])
        return rdd
