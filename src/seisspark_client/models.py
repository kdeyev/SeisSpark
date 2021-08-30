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
import inspect
import io
import sys
from typing import Any  # noqa
from typing import List, Optional

from pydantic import BaseModel, Field


class CreateModuleRequest(BaseModel):
    module_type: "str" = Field(..., alias="module_type")
    name: "Optional[str]" = Field(None, alias="name")
    prev_module_id: "Optional[str]" = Field(None, alias="prev_module_id")


class CreatePipelineRequest(BaseModel):
    name: "str" = Field(..., alias="name")


class HTTPValidationError(BaseModel):
    detail: "Optional[List[ValidationError]]" = Field(None, alias="detail")


class ModuleDescription(BaseModel):
    id: "str" = Field(..., alias="id")
    name: "str" = Field(..., alias="name")
    params_schema: "Any" = Field(..., alias="params_schema")


class ModuleInfo(BaseModel):
    id: "str" = Field(..., alias="id")
    name: "str" = Field(..., alias="name")


class MoveModuleRequest(BaseModel):
    module_id: "str" = Field(..., alias="module_id")
    prev_module_id: "Optional[str]" = Field(None, alias="prev_module_id")


class PipelineInfo(BaseModel):
    id: "str" = Field(..., alias="id")
    name: "str" = Field(..., alias="name")


class ValidationError(BaseModel):
    loc: "List[str]" = Field(..., alias="loc")
    msg: "str" = Field(..., alias="msg")
    type: "str" = Field(..., alias="type")


IO = io.IOBase

current_module = sys.modules[__name__]

for model in inspect.getmembers(current_module, inspect.isclass):
    model_class = model[1]
    if isinstance(model_class, BaseModel) or hasattr(model_class, "update_forward_refs"):
        model_class.update_forward_refs()
