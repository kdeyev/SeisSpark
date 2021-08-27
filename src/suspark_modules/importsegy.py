from typing import Optional, cast

import pydantic
import pyspark

from su_rdd.kv_operations import GatherTuple
from su_rdd.rdd_operations import import_segy_to_rdd
from suspark.suspark_context import SusparkContext
from suspark.suspark_module import BaseModule


class ImpotSegyParams(pydantic.BaseModel):
    filepath: str = "/root/SeisSpark/Line_001_ieee.sgy"
    chunk_size: int = 100


class ImportSegy(BaseModule):
    def __init__(self, id: str, name: str) -> None:
        super().__init__(id=id, name=name, paramsModel=ImpotSegyParams, params=ImpotSegyParams())

    @property
    def importsegy_params(self) -> ImpotSegyParams:
        return cast(ImpotSegyParams, self.parameters)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        if input_rdd:
            raise Exception("input RDD is not used")

        rdd = import_segy_to_rdd(suspark_context.context, file_path=self.importsegy_params.filepath, chunk_size=self.importsegy_params.chunk_size)
        return rdd
