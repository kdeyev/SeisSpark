from typing import Optional, cast

import pydantic
import pyspark

from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_rdd.rdd_operations import select_by_trace_header
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SelectTracesParams(pydantic.BaseModel):
    key: SEGYTraceHeaderEntryName = SEGYTraceHeaderEntryName.TraceIdenitifactionCode
    value: int = 1


class SelectTraces(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SelectTracesParams, params=SelectTracesParams())

    @property
    def select_traces_params(self) -> SelectTracesParams:
        return cast(SelectTracesParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")
        key: SEGYTraceHeaderEntryName = self.select_traces_params.key
        value: int = self.select_traces_params.value

        rdd = select_by_trace_header(input_rdd, SEGY_TRACE_HEADER_ENTRIES[key], value)
        return rdd
