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
from typing import TYPE_CHECKING, Any, Awaitable, List

from fastapi.encoders import jsonable_encoder

from seisspark_client import models as m

if TYPE_CHECKING:
    from seisspark_client.api_client import ApiClient


class _PipelinesApi:
    def __init__(self, api_client: "ApiClient"):
        self.api_client = api_client

    def _build_for_create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(self, pipeline_id: str, create_module_request: m.CreateModuleRequest) -> Awaitable[m.ModuleDescription]:
        path_params = {"pipeline_id": str(pipeline_id)}

        body = jsonable_encoder(create_module_request, exclude_defaults=True)

        return self.api_client.request(
            type_=m.ModuleDescription,
            method="POST",
            url="/api/v1/pipelines/{pipeline_id}/modules",
            path_params=path_params,
            json=body,
        )

    def _build_for_create_pipelines_api_v1_pipelines_post(self, create_pipeline_request: m.CreatePipelineRequest) -> Awaitable[m.PipelineInfo]:
        body = jsonable_encoder(create_pipeline_request, exclude_defaults=True)

        return self.api_client.request(type_=m.PipelineInfo, method="POST", url="/api/v1/pipelines", json=body)

    def _build_for_delete_pipeline_api_v1_pipelines_pipeline_id_delete(self, pipeline_id: str) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id)}

        return self.api_client.request(
            type_=m.Any,
            method="DELETE",
            url="/api/v1/pipelines/{pipeline_id}",
            path_params=path_params,
        )

    def _build_for_delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(self, pipeline_id: str, module_id: str) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id), "module_id": str(module_id)}

        return self.api_client.request(
            type_=m.Any,
            method="DELETE",
            url="/api/v1/pipelines/{pipeline_id}/modules/{module_id}",
            path_params=path_params,
        )

    def _build_for_get_pipeline_api_v1_pipelines_pipeline_id_get(self, pipeline_id: str) -> Awaitable[m.PipelineInfo]:
        path_params = {"pipeline_id": str(pipeline_id)}

        return self.api_client.request(
            type_=m.PipelineInfo,
            method="GET",
            url="/api/v1/pipelines/{pipeline_id}",
            path_params=path_params,
        )

    def _build_for_get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(self, pipeline_id: str, module_id: str, key: int) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id), "module_id": str(module_id), "key": str(key)}

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/api/v1/pipelines/{pipeline_id}/modules/{module_id}/data/{key}",
            path_params=path_params,
        )

    def _build_for_get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(self, pipeline_id: str, module_id: str) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id), "module_id": str(module_id)}

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/api/v1/pipelines/{pipeline_id}/modules/{module_id}/keys",
            path_params=path_params,
        )

    def _build_for_get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(self, pipeline_id: str, module_id: str) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id), "module_id": str(module_id)}

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters",
            path_params=path_params,
        )

    def _build_for_get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(self, pipeline_id: str, module_id: str) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id), "module_id": str(module_id)}

        return self.api_client.request(
            type_=m.Any,
            method="GET",
            url="/api/v1/pipelines/{pipeline_id}/modules/{module_id}/schema",
            path_params=path_params,
        )

    def _build_for_get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(self, pipeline_id: str) -> Awaitable[List[m.ModuleInfo]]:
        path_params = {"pipeline_id": str(pipeline_id)}

        return self.api_client.request(
            type_=List[m.ModuleInfo],
            method="GET",
            url="/api/v1/pipelines/{pipeline_id}/modules",
            path_params=path_params,
        )

    def _build_for_get_pipelines_api_v1_pipelines_get(
        self,
    ) -> Awaitable[List[m.PipelineInfo]]:
        return self.api_client.request(
            type_=List[m.PipelineInfo],
            method="GET",
            url="/api/v1/pipelines",
        )

    def _build_for_move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(self, pipeline_id: str, move_module_request: m.MoveModuleRequest) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id)}

        body = jsonable_encoder(move_module_request, exclude_defaults=True)

        return self.api_client.request(type_=m.Any, method="PUT", url="/api/v1/pipelines/{pipeline_id}/modules", path_params=path_params, json=body)

    def _build_for_set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(self, pipeline_id: str, module_id: str, body: Any) -> Awaitable[m.Any]:
        path_params = {"pipeline_id": str(pipeline_id), "module_id": str(module_id)}

        body = jsonable_encoder(body, exclude_defaults=True)

        return self.api_client.request(
            type_=m.Any,
            method="PUT",
            url="/api/v1/pipelines/{pipeline_id}/modules/{module_id}/parameters",
            path_params=path_params,
            json=body,
        )


class AsyncPipelinesApi(_PipelinesApi):
    async def create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(self, pipeline_id: str, create_module_request: m.CreateModuleRequest) -> m.ModuleDescription:
        return await self._build_for_create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(pipeline_id=pipeline_id, create_module_request=create_module_request)

    async def create_pipelines_api_v1_pipelines_post(self, create_pipeline_request: m.CreatePipelineRequest) -> m.PipelineInfo:
        return await self._build_for_create_pipelines_api_v1_pipelines_post(create_pipeline_request=create_pipeline_request)

    async def delete_pipeline_api_v1_pipelines_pipeline_id_delete(self, pipeline_id: str) -> m.Any:
        return await self._build_for_delete_pipeline_api_v1_pipelines_pipeline_id_delete(pipeline_id=pipeline_id)

    async def delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(self, pipeline_id: str, module_id: str) -> m.Any:
        return await self._build_for_delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(pipeline_id=pipeline_id, module_id=module_id)

    async def get_pipeline_api_v1_pipelines_pipeline_id_get(self, pipeline_id: str) -> m.PipelineInfo:
        return await self._build_for_get_pipeline_api_v1_pipelines_pipeline_id_get(pipeline_id=pipeline_id)

    async def get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(self, pipeline_id: str, module_id: str, key: int) -> m.Any:
        return await self._build_for_get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(pipeline_id=pipeline_id, module_id=module_id, key=key)

    async def get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(self, pipeline_id: str, module_id: str) -> m.Any:
        return await self._build_for_get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(pipeline_id=pipeline_id, module_id=module_id)

    async def get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(self, pipeline_id: str, module_id: str) -> m.Any:
        return await self._build_for_get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(pipeline_id=pipeline_id, module_id=module_id)

    async def get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(self, pipeline_id: str, module_id: str) -> m.Any:
        return await self._build_for_get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(pipeline_id=pipeline_id, module_id=module_id)

    async def get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(self, pipeline_id: str) -> List[m.ModuleInfo]:
        return await self._build_for_get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(pipeline_id=pipeline_id)

    async def get_pipelines_api_v1_pipelines_get(
        self,
    ) -> List[m.PipelineInfo]:
        return await self._build_for_get_pipelines_api_v1_pipelines_get()

    async def move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(self, pipeline_id: str, move_module_request: m.MoveModuleRequest) -> m.Any:
        return await self._build_for_move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(pipeline_id=pipeline_id, move_module_request=move_module_request)

    async def set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(self, pipeline_id: str, module_id: str, body: Any) -> m.Any:
        return await self._build_for_set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(pipeline_id=pipeline_id, module_id=module_id, body=body)


class SyncPipelinesApi(_PipelinesApi):
    def create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(self, pipeline_id: str, create_module_request: m.CreateModuleRequest) -> m.ModuleDescription:
        coroutine = self._build_for_create_pipeline_module_api_v1_pipelines_pipeline_id_modules_post(pipeline_id=pipeline_id, create_module_request=create_module_request)
        return get_event_loop().run_until_complete(coroutine)

    def create_pipelines_api_v1_pipelines_post(self, create_pipeline_request: m.CreatePipelineRequest) -> m.PipelineInfo:
        coroutine = self._build_for_create_pipelines_api_v1_pipelines_post(create_pipeline_request=create_pipeline_request)
        return get_event_loop().run_until_complete(coroutine)

    def delete_pipeline_api_v1_pipelines_pipeline_id_delete(self, pipeline_id: str) -> m.Any:
        coroutine = self._build_for_delete_pipeline_api_v1_pipelines_pipeline_id_delete(pipeline_id=pipeline_id)
        return get_event_loop().run_until_complete(coroutine)

    def delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(self, pipeline_id: str, module_id: str) -> m.Any:
        coroutine = self._build_for_delete_pipeline_module_api_v1_pipelines_pipeline_id_modules_module_id_delete(pipeline_id=pipeline_id, module_id=module_id)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipeline_api_v1_pipelines_pipeline_id_get(self, pipeline_id: str) -> m.PipelineInfo:
        coroutine = self._build_for_get_pipeline_api_v1_pipelines_pipeline_id_get(pipeline_id=pipeline_id)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(self, pipeline_id: str, module_id: str, key: int) -> m.Any:
        coroutine = self._build_for_get_pipeline_module_data_api_v1_pipelines_pipeline_id_modules_module_id_data_key_get(pipeline_id=pipeline_id, module_id=module_id, key=key)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(self, pipeline_id: str, module_id: str) -> m.Any:
        coroutine = self._build_for_get_pipeline_module_data_info_api_v1_pipelines_pipeline_id_modules_module_id_keys_get(pipeline_id=pipeline_id, module_id=module_id)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(self, pipeline_id: str, module_id: str) -> m.Any:
        coroutine = self._build_for_get_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_get(pipeline_id=pipeline_id, module_id=module_id)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(self, pipeline_id: str, module_id: str) -> m.Any:
        coroutine = self._build_for_get_pipeline_module_schema_api_v1_pipelines_pipeline_id_modules_module_id_schema_get(pipeline_id=pipeline_id, module_id=module_id)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(self, pipeline_id: str) -> List[m.ModuleInfo]:
        coroutine = self._build_for_get_pipeline_modules_api_v1_pipelines_pipeline_id_modules_get(pipeline_id=pipeline_id)
        return get_event_loop().run_until_complete(coroutine)

    def get_pipelines_api_v1_pipelines_get(
        self,
    ) -> List[m.PipelineInfo]:
        coroutine = self._build_for_get_pipelines_api_v1_pipelines_get()
        return get_event_loop().run_until_complete(coroutine)

    def move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(self, pipeline_id: str, move_module_request: m.MoveModuleRequest) -> m.Any:
        coroutine = self._build_for_move_pipeline_module_api_v1_pipelines_pipeline_id_modules_put(pipeline_id=pipeline_id, move_module_request=move_module_request)
        return get_event_loop().run_until_complete(coroutine)

    def set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(self, pipeline_id: str, module_id: str, body: Any) -> m.Any:
        coroutine = self._build_for_set_pipeline_module_parameters_api_v1_pipelines_pipeline_id_modules_module_id_parameters_put(pipeline_id=pipeline_id, module_id=module_id, body=body)
        return get_event_loop().run_until_complete(coroutine)
