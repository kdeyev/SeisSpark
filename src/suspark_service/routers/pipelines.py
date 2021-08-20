from fastapi import APIRouter, Path

from suspark.pipeline_repository import PiplineRepository


def init_router(pipeline_repository: PiplineRepository) -> APIRouter:
    router = APIRouter()

    @router.get("/pipelines", tags=["pipelines"])
    def get_pipelines():
        pass

    @router.get("/pipelines/{pipeline_id}", tags=["pipelines"])
    def get_pipeline(pipeline_id: str = Path(...)):
        pass

    @router.get("/pipelines/{pipeline_id}/modules", tags=["pipelines"])
    def get_pipeline(pipeline_id: str = Path(...)):
        pass

    return router
