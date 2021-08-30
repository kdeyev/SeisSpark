from fastapi import FastAPI

import seisspark_service.routers.modules as modules
import seisspark_service.routers.pipelines as pipelines
from seisspark.pipeline_repository import PiplineRepository
from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark_service.inferring_router import InferringRouter


def create_seisspark_service_app(modules_factory: ModulesFactory, pipeline_repository: PiplineRepository) -> FastAPI:

    app = FastAPI()

    router = InferringRouter(prefix="/api/v1")
    router.include_router(pipelines.init_router(pipeline_repository=pipeline_repository))
    router.include_router(modules.init_router(modules_factory=modules_factory))

    app.include_router(router)

    # @app.on_event("startup")
    # async def startup() -> None:
    #     await db_handler.connect()

    return app
