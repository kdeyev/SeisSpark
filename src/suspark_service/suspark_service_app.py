from fastapi import APIRouter, FastAPI

import suspark_service.routers.modules as modules
import suspark_service.routers.pipelines as pipelines
from suspark.pipeline_repository import PiplineRepository
from suspark.suspark_modules_factory import ModulesFactory


def create_suspark_service_app(modules_factory: ModulesFactory, pipeline_repository: PiplineRepository) -> FastAPI:

    app = FastAPI()

    router = APIRouter(prefix="/api/v1")
    router.include_router(pipelines.init_router(pipeline_repository=pipeline_repository))
    router.include_router(modules.init_router(modules_factory=modules_factory))

    app.include_router(router)

    # @app.on_event("startup")
    # async def startup() -> None:
    #     await db_handler.connect()

    return app
