from os import name
from typing import Any, Dict, List, Optional

import pydantic
from fastapi import APIRouter, Body, Path
from fastapi.responses import JSONResponse

from suspark.pipeline_repository import PipelineInfo, PiplineRepository, PiplineRepositoryItem
from suspark.suspark_module import BaseModule
from suspark_service.inferring_router import InferringRouter


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


def init_router(pipeline_repository: PiplineRepository) -> InferringRouter:
    router = InferringRouter()

    @router.get("/pipelines", tags=["pipelines"])
    def get_pipelines() -> List[PipelineInfo]:
        return pipeline_repository.get_pipeline_ids()

    @router.post("/pipelines", tags=["pipelines"])
    def create_pipelines(pipeline: CreatePipelineRequest) -> PipelineInfo:
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
    def create_pipeline_modules(
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

    return router
