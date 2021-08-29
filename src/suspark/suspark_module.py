import json
from typing import Any, Dict, Optional, Type, cast

import pydantic
import pyspark

from su_rdd.kv_operations import GatherTuple
from suspark.suspark_context import SusparkContext


class BaseModule:
    def __init__(self, id: str, name: str, paramsModel: Type[pydantic.BaseModel] = pydantic.BaseModel, params: Optional[pydantic.BaseModel] = None) -> None:
        self._id = id  # str(uuid.uuid4())
        self._name = name
        self._paramsModel = paramsModel
        self._params = params
        self._rdd: Optional["pyspark.RDD[GatherTuple]"] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def rdd(self) -> "pyspark.RDD[GatherTuple]":
        if not self._rdd:
            raise Exception("RDD is not initialized")
        return self._rdd

    def invalidate_rdd(self) -> None:
        self._rdd = None

    @property
    def params_schema(self) -> Dict[str, Any]:
        return cast(Dict[str, Any], json.loads(self._paramsModel.schema_json()))

    @property
    def parameters(self) -> pydantic.BaseModel:
        if not self._params:
            raise Exception("params are not initialized")
        return self._params

    def set_paramters(self, params: pydantic.BaseModel) -> None:
        if type(params) != self._paramsModel:
            raise Exception("Wrong parameters type")
        self._params = params

    def set_json_parameters(self, json: Dict[str, Any]) -> None:
        self._params = self._paramsModel(**json)

    def _init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        raise Exception("Not implemented")

    def init_rdd(self, suspark_context: SusparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> None:
        self._rdd = self._init_rdd(suspark_context, input_rdd)
