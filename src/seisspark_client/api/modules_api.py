# flake8: noqa E501
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
from asyncio import get_event_loop
from typing import TYPE_CHECKING, Awaitable, List

from seisspark_client import models as m

if TYPE_CHECKING:
    from seisspark_client.api_client import ApiClient


class _ModulesApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_get_module_schema_api_v1_modules_module_type_get(self, module_type: str) -> Awaitable[m.Any]:
        path_params = {"module_type": str(module_type)}

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/api/v1/modules/{module_type}",
            path_params=path_params,
        )

    def _build_for_get_modules_api_v1_modules_get(
        self,
    ) -> Awaitable[List[str]]:
        return self.api_client.request(
            type_=List[str],
            method="GET",
            url="/api/v1/modules",
        )


class AsyncModulesApi(_ModulesApi):
    async def get_module_schema_api_v1_modules_module_type_get(self, module_type: str) -> m.Any:
        return await self._build_for_get_module_schema_api_v1_modules_module_type_get(module_type=module_type)

    async def get_modules_api_v1_modules_get(
        self,
    ) -> List[str]:
        return await self._build_for_get_modules_api_v1_modules_get()


class SyncModulesApi(_ModulesApi):
    def get_module_schema_api_v1_modules_module_type_get(self, module_type: str) -> m.Any:
        coroutine = self._build_for_get_module_schema_api_v1_modules_module_type_get(module_type=module_type)
        return get_event_loop().run_until_complete(coroutine)

    def get_modules_api_v1_modules_get(
        self,
    ) -> List[str]:
        coroutine = self._build_for_get_modules_api_v1_modules_get()
        return get_event_loop().run_until_complete(coroutine)
