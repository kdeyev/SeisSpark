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
from typing import Any, Dict, List, Optional, Type, cast

import pydantic
import pyspark

from seisspark.seisspark_context import SeisSparkContext
from su_rdd.kv_operations import GatherTuple


class SocketDescription(pydantic.BaseModel):
    name: str


class BaseModule:
    def __init__(
        self,
        id: str,
        name: str,
        input_sockets: List[SocketDescription] = [],
        output_sockets: List[SocketDescription] = [],
        params_model: Type[pydantic.BaseModel] = pydantic.BaseModel,
        params: Optional[pydantic.BaseModel] = None,
    ) -> None:
        self._id = id
        self._name = name
        self._input_sockets = input_sockets
        self._output_sockets = output_sockets
        self._params_model = params_model
        self._params = params
        self._rdd: Optional["pyspark.RDD[GatherTuple]"] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def input_sockets(self) -> List[SocketDescription]:
        return self._input_sockets

    @property
    def output_sockets(self) -> List[SocketDescription]:
        return self._output_sockets

    # @property
    # def rdd(self) -> "pyspark.RDD[GatherTuple]":
    #     if not self._rdd:
    #         raise Exception("RDD is not initialized")
    #     return self._rdd

    # def invalidate_rdd(self) -> None:
    #     self._rdd = None

    @property
    def params_schema(self) -> Dict[str, Any]:
        return cast(Dict[str, Any], json.loads(self._params_model.schema_json()))

    @property
    def parameters(self) -> pydantic.BaseModel:
        if not self._params:
            raise Exception("params are not initialized")
        return self._params

    def set_paramters(self, params: pydantic.BaseModel) -> None:
        if type(params) != self._params_model:
            raise Exception("Wrong parameters type")
        self._params = params

    def set_json_parameters(self, json: Dict[str, Any]) -> None:
        self._params = self._params_model(**json)

    def init_rdd(self, seisspark_context: SeisSparkContext, input_rdds: List[Optional["pyspark.RDD[GatherTuple]"]]) -> List[Optional["pyspark.RDD[GatherTuple]"]]:
        raise Exception("Not implemented")

    # def init_rdd(self, seisspark_context: SeisSparkContext, input_rdd: Optional["pyspark.RDD[GatherTuple]"]) -> None:
    #     self._rdd = self._init_rdd(seisspark_context, input_rdd)
