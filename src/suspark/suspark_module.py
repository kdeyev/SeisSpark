import json
import uuid
from typing import Any, Dict, Optional, Type

import pydantic
import pyspark

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
