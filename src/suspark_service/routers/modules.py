from fastapi import APIRouter, Path

from suspark.suspark_modules_factory import ModulesFactory


def init_router(modules_factory: ModulesFactory) -> APIRouter:
    router = APIRouter()

    @router.get("/modules", tags=["modules"])
    def get_modules():
        return modules_factory.get_module_types()

    @router.get("/modules/{module_type}", tags=["modules"])
    def get_module_schema(module_type: str = Path(...)):
        schema = modules_factory.get_module_params_json_schema(module_type)
        return schema

    return router
