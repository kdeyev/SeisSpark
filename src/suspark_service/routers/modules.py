from typing import Any, Dict, List

from fastapi import Path

from suspark.suspark_modules_factory import ModulesFactory
from suspark_service.inferring_router import InferringRouter


def init_router(modules_factory: ModulesFactory) -> InferringRouter:
    router = InferringRouter()

    @router.get("/modules", tags=["modules"])
    def get_modules() -> List[str]:
        return modules_factory.get_module_types()

    @router.get("/modules/{module_type}", tags=["modules"])
    def get_module_schema(module_type: str = Path(...)) -> Dict[str, Any]:
        return modules_factory.get_module_params_json_schema(module_type)

    return router
