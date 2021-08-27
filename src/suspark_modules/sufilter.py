from typing import List, Optional, cast

import pydantic
import pyspark

from su_rdd.kv_operations import GatherTuple
from su_rdd.rdd_operations import su_process_rdd
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUFilterFA(pydantic.BaseModel):
    f: float
    a: float


class SUFilterParams(pydantic.BaseModel):
    filter: List[SUFilterFA] = [SUFilterFA(f=10, a=0), SUFilterFA(f=20, a=1), SUFilterFA(f=30, a=1), SUFilterFA(f=40, a=0)]


class SUfilter(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SUFilterParams, params=SUFilterParams())

    @property
    def sufilter_params(self) -> SUFilterParams:
        return cast(SUFilterParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        if not input_rdd:
            raise Exception("input RDD should be specified")
        # key: SEGYTraceHeaderEntryName = self.sufilter_params.key

        f = ",".join([f"{val.f}" for val in self.sufilter_params.filter])
        a = ",".join([f"{val.a}" for val in self.sufilter_params.filter])
        args = []
        if f:
            args.append(f"f={f}")
        if a:
            args.append(f"a={a}")
        rdd = su_process_rdd(input_rdd, "sufilter", args)
        return rdd
