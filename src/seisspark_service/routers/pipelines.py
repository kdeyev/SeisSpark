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
from typing import Any, Dict, List, Optional

import pydantic
from fastapi import Body, Path
from fastapi.responses import JSONResponse

from seisspark.pipeline_repository import PipelineInfo, PiplineRepository, PiplineRepositoryItem
from seisspark.seisspark_module import BaseModule
from seisspark_service.inferring_router import InferringRouter
from su_rdd.kv_operations import gather_from_rdd_gather_tuple
from su_rdd.rdd_operations import get_gather_by_key, get_gather_keys


class CreatePipelineRequest(pydantic.BaseModel):
    name: str


# class CreatePipelineResponse(pydantic.BaseModel):
#     id: str


class ModuleInfo(pydantic.BaseModel):
    id: str
    name: str


class ModuleDescription(ModuleInfo):
    params_schema: Dict[str, Any]


class PipelineDescription(PipelineInfo):
    modules: List[ModuleInfo]


class CreateModuleRequest(pydantic.BaseModel):
    module_type: str
    name: Optional[str] = None
    prev_module_id: Optional[str] = None


class MoveModuleRequest(pydantic.BaseModel):
    module_id: str
    prev_module_id: Optional[str] = None


def init_router(pipeline_repository: PiplineRepository) -> InferringRouter:
    router = InferringRouter()

    @router.get("/pipelines", tags=["pipelines"])
    def get_pipelines() -> List[PipelineInfo]:
        return pipeline_repository.get_pipeline_ids()

    @router.post("/pipelines", tags=["pipelines"])
    def create_pipeline(pipeline: CreatePipelineRequest) -> PipelineInfo:
        id = pipeline_repository.add_pipeline(name=pipeline.name)
        return PipelineInfo(id=id, name=pipeline.name)

    @router.delete("/pipelines/{pipeline_id}", tags=["pipelines"])
    def delete_pipeline(pipeline_id: str = Path(...)) -> JSONResponse:
        pipeline_repository.delete_pipeline(id=pipeline_id)
        return JSONResponse({"status": "Ok"})

    @router.get("/pipelines/{pipeline_id}", tags=["pipelines"])
    def get_pipeline(pipeline_id: str = Path(...)) -> PipelineInfo:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        pipeline_modules: List[ModuleInfo] = []
        for module in item.pipeline.modules():
            pipeline_modules.append(ModuleInfo(id=module.id, name=module.name))
        return PipelineDescription(id=item.id, name=item.name, modules=pipeline_modules)

    @router.get("/pipelines/{pipeline_id}/modules", tags=["pipelines"])
    def get_pipeline_modules(pipeline_id: str = Path(...)) -> List[ModuleInfo]:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        pipeline_modules: List[ModuleInfo] = []
        for module in item.pipeline.modules():
            pipeline_modules.append(ModuleInfo(id=module.id, name=module.name))
        return pipeline_modules

    @router.post("/pipelines/{pipeline_id}/modules", tags=["pipelines"])
    def create_pipeline_module(
        pipeline_id: str = Path(...),
        module_request: CreateModuleRequest = Body(...),
    ) -> ModuleDescription:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        module: BaseModule = item.pipeline.add_module(module_type=module_request.module_type, name=module_request.name, prev_module_id=module_request.prev_module_id)
        return ModuleDescription(
            id=module.id,
            name=module.name,
            params_schema=module.params_schema,
        )

    @router.put("/pipelines/{pipeline_id}/modules", tags=["pipelines"])
    def move_pipeline_module(
        pipeline_id: str = Path(...),
        module_request: MoveModuleRequest = Body(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        item.pipeline.move_module(module_id=module_request.module_id, prev_module_id=module_request.prev_module_id)
        return JSONResponse({"status": "Ok"})

    @router.delete("/pipelines/{pipeline_id}/modules/{module_id}", tags=["pipelines"])
    def delete_pipeline_module(
        pipeline_id: str = Path(...),
        module_id: str = Path(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        item.pipeline.delete_module(module_id=module_id)
        return JSONResponse({"status": "Ok"})

    @router.get("/pipelines/{pipeline_id}/modules/{module_id}/parameters", tags=["pipelines"])
    def get_pipeline_module_parameters(
        pipeline_id: str = Path(...),
        module_id: str = Path(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        module: BaseModule = item.pipeline.get_module(module_id=module_id)
        return JSONResponse(module.parameters.dict())

    @router.put("/pipelines/{pipeline_id}/modules/{module_id}/parameters", tags=["pipelines"])
    def set_pipeline_module_parameters(
        pipeline_id: str = Path(...),
        module_id: str = Path(...),
        parameters: Dict[str, Any] = Body(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        module: BaseModule = item.pipeline.get_module(module_id=module_id)
        module.set_json_parameters(parameters)
        # FIXME:
        item.pipeline._init_rdd()
        return JSONResponse(module.parameters.dict())

    @router.get("/pipelines/{pipeline_id}/modules/{module_id}/schema", tags=["pipelines"])
    def get_pipeline_module_schema(
        pipeline_id: str = Path(...),
        module_id: str = Path(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        module: BaseModule = item.pipeline.get_module(module_id=module_id)
        return JSONResponse(module.params_schema)

    @router.get("/pipelines/{pipeline_id}/modules/{module_id}/keys", tags=["pipelines"])
    def get_pipeline_module_data_info(
        pipeline_id: str = Path(...),
        module_id: str = Path(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        module: BaseModule = item.pipeline.get_module(module_id=module_id)
        keys = get_gather_keys(module.rdd)
        return JSONResponse(keys)

    @router.get("/pipelines/{pipeline_id}/modules/{module_id}/data/{key}", tags=["pipelines"])
    def get_pipeline_module_data(
        pipeline_id: str = Path(...),
        module_id: str = Path(...),
        key: int = Path(...),
    ) -> JSONResponse:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        module: BaseModule = item.pipeline.get_module(module_id=module_id)
        value = get_gather_by_key(module.rdd, key)
        first_gather = gather_from_rdd_gather_tuple((key, value))
        gather_data = first_gather.get_data_array()
        return JSONResponse(gather_data)

    return router
