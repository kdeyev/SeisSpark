# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
import json
from typing import Any, Dict, Optional, Type, cast

import pydantic
import pyspark

from seisspark.seisspark_context import SeisSparkContext
from su_rdd.kv_operations import GatherTuple


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

    def _init_rdd(self, seisspark_context: SeisSparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> "pyspark.RDD[GatherTuple]":
        raise Exception("Not implemented")

    def init_rdd(self, seisspark_context: SeisSparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> None:
        self._rdd = self._init_rdd(seisspark_context, input_rdd)
