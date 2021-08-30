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

from pydantic import BaseModel

from seisspark_client import models
from seisspark_client.api_client import ApiClient, AsyncApis, SyncApis  # noqa F401
from seisspark_client.exceptions import ApiException, UnexpectedResponse  # noqa F401

for model in inspect.getmembers(models, inspect.isclass):
    if model[1].__module__ == "seisspark_client.models":
        model_class = model[1]
        if isinstance(model_class, BaseModel):
            model_class.update_forward_refs()
