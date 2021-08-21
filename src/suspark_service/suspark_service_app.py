import configargparse
import uvicorn
from fastapi import FastAPI

import suspark_service.routers.modules as modules
import suspark_service.routers.pipelines as pipelines
from suspark.pipeline_repository import PiplineRepository
from suspark.suspark_context import SusparkContext
from suspark.suspark_modules_factory import ModulesFactory, register_module_types


def create_suspark_service_app() -> FastAPI:

    app = FastAPI()
    modules_factory = ModulesFactory()
    suspark_context = SusparkContext()
    pipeline_repository = PiplineRepository(suspark_context=suspark_context, modules_factory=modules_factory)
    register_module_types(modules_factory)

    app.include_router(pipelines.init_router(pipeline_repository=pipeline_repository))
    app.include_router(modules.init_router(modules_factory=modules_factory))

    # @app.on_event("startup")
    # async def startup() -> None:
    #     await db_handler.connect()

    return app
