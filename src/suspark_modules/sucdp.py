from typing import Optional

import pydantic
import pyspark

from su_rdd.rdd_operations import su_process_rdd
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUcdpParams(pydantic.BaseModel):
    pass


class SUcdp(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SUcdpParams, params=SUcdpParams())

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")

        rdd = su_process_rdd(input_rdd, "suchw", ["key1=cdp", "key2=gx", "key3=sx", "b=1", "c=1", "d=2"])
        return rdd
