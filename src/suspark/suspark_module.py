import json
import uuid
from typing import Any, Dict, List, Optional, Type, cast

import pydantic
import pyspark

from su_data.segy_trace_header import SEGY_TRACE_HEADER_ENTRIES, SEGYTraceHeaderEntryName
from su_data.su_pipe import su_process_pipe
from su_rdd.kv_operations import gather_from_rdd_key_value, rdd_key_value_from_gather
from su_rdd.rdd_operations import group_by_trace_header, su_process_rdd
from suspark.suspark_context import SusparkContext


class BaseModule:
    def __init__(self, paramsModel: Type[pydantic.BaseModel], params: Optional[pydantic.BaseModel] = None) -> None:
        self._id = str(uuid.uuid4())
        self._paramsModel = paramsModel
        self._params = params
        self._rdd: Optional[pyspark.RDD] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def rdd(self) -> pyspark.RDD:
        if not self._rdd:
            raise Exception("RDD is not initialized")
        return self._rdd

    def invalidate_rdd(self) -> None:
        self._rdd = None

    @property
    def json_schema(self) -> Any:
        return json.loads(self._paramsModel.schema_json())

    @property
    def parameters(self) -> Any:
        if not self._params:
            raise Exception("params are not initialized")
        return self._params

    def set_paramters(self, params: pydantic.BaseModel) -> None:
        if type(params) != self._paramsModel:
            raise Exception("Wrong parameters type")
        self._params = params

    def set_json_parameters(self, json: Dict[str, Any]) -> None:
        self._params = self._paramsModel(**json)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        raise Exception("Not implemented")

    def init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> None:
        self._rdd = self._init_rdd(suspark_context, input_rdd)


class SUimp2d(BaseModule):
    class SUimp2dParams(pydantic.BaseModel):
        nshot: int = 1
        nrec: int = 1

    def __init__(self) -> None:
        super().__init__(SUimp2d.SUimp2dParams, SUimp2d.SUimp2dParams())

    @property
    def suimp2d_params(self) -> "SUimp2d.SUimp2dParams":
        return cast(SUimp2d.SUimp2dParams, self.parameters)

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


class SUsort(BaseModule):
    class SUsortParams(pydantic.BaseModel):
        key: SEGYTraceHeaderEntryName = SEGYTraceHeaderEntryName.FieldRecord

    def __init__(self) -> None:
        super().__init__(SUsort.SUsortParams, SUsort.SUsortParams())

    @property
    def susort_params(self) -> "SUsort.SUsortParams":
        return cast(SUsort.SUsortParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")
        key: SEGYTraceHeaderEntryName = self.susort_params.key

        rdd = group_by_trace_header(input_rdd, SEGY_TRACE_HEADER_ENTRIES[key])
        return rdd


class SUFilterFA(pydantic.BaseModel):
    f: float
    a: float


class SUFilterParams(pydantic.BaseModel):
    filter: List[SUFilterFA] = []


class SUfilter(BaseModule):
    def __init__(self) -> None:
        super().__init__(SUFilterParams, SUFilterParams())

    @property
    def sufilter_params(self) -> SUFilterParams:
        return cast(SUFilterParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")
        # key: SEGYTraceHeaderEntryName = self.sufilter_params.key

        rdd = su_process_rdd(input_rdd, "sufilter", ["f1=10,f2=20,f3=30,f4-40"])
        return rdd
