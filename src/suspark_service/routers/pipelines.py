from os import name
from typing import List

import pydantic
from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse

from suspark.pipeline_repository import PipelineInfo, PiplineRepository, PiplineRepositoryItem


class CreatePipelineRequest(pydantic.BaseModel):
    name: str


class CreatePipelineResponse(pydantic.BaseModel):
    id: str


class ModuleInfo(pydantic.BaseModel):
    id: str
    name: str


class PipelineModules(pydantic.BaseModel):
    modules: List[ModuleInfo]


def init_router(pipeline_repository: PiplineRepository) -> APIRouter:
    router = APIRouter()

    @router.get("/pipelines", tags=["pipelines"])
    def get_pipelines() -> List[PipelineInfo]:
        return pipeline_repository.get_pipeline_ids()

    @router.post("/pipelines", tags=["pipelines"])
    def create_pipelines(pipeline: CreatePipelineRequest) -> CreatePipelineResponse:
        id = pipeline_repository.add_pipeline(name=pipeline.name)
        return CreatePipelineResponse(id=id)

    @router.delete("/pipelines/{pipeline_id}", tags=["pipelines"])
    def delete_pipeline(pipeline_id: str = Path(...)) -> JSONResponse:
        pipeline_repository.delete_pipeline(id=pipeline_id)
        return JSONResponse({"status": "Ok"})

    @router.get("/pipelines/{pipeline_id}", tags=["pipelines"])
    def get_pipeline(pipeline_id: str = Path(...)) -> List[ModuleInfo]:
        item: PiplineRepositoryItem = pipeline_repository.get_pipeline(id=pipeline_id)
        pipeline_modules: List[ModuleInfo] = []
        for module in item.pipeline.modules():
            pipeline_modules.append(ModuleInfo(id=module.id, name=module.name))
        return pipeline_modules

    # @router.get("/pipelines/{pipeline_id}/modules", tags=["pipelines"])
    # def get_pipeline_modules(pipeline_id: str = Path(...)):
    #     pass

    return router
