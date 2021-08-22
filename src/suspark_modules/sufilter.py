from typing import List, Optional, cast

import pydantic
import pyspark

from su_rdd.rdd_operations import su_process_rdd
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUFilterFA(pydantic.BaseModel):
    f: float
    a: float


class SUFilterParams(pydantic.BaseModel):
    filter: List[SUFilterFA] = []


class SUfilter(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SUFilterParams, params=SUFilterParams())

    @property
    def sufilter_params(self) -> SUFilterParams:
        return cast(SUFilterParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")
        # key: SEGYTraceHeaderEntryName = self.sufilter_params.key

        rdd = su_process_rdd(input_rdd, "sufilter", ["f1=10,f2=20,f3=30,f4-40"])
        return rdd
