from typing import List, Optional, cast

import pydantic
import pyspark

from su_rdd.rdd_operations import su_process_rdd
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class SUagcParams(pydantic.BaseModel):
    pass


class SUagc(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=SUagcParams, params=SUagcParams())

    @property
    def suagc_params(self) -> SUagcParams:
        return cast(SUagcParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional[pyspark.RDD]) -> pyspark.RDD:
        if not input_rdd:
            raise Exception("input RDD should be specified")

        rdd = su_process_rdd(input_rdd, "suagc", ["agc=1"])
        return rdd
