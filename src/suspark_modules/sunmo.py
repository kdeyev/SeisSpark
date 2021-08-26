from typing import Optional

import pydantic
import pyspark

from su_rdd.kv_operations import GatherTuple
from su_rdd.rdd_operations import su_process_rdd
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUnmoParams(pydantic.BaseModel):
    pass


class SUnmo(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SUnmoParams, params=SUnmoParams())

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        if not input_rdd:
            raise Exception("input RDD should be specified")

        rdd = su_process_rdd(input_rdd, "sunmo", [])
        return rdd
