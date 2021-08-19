from fastapi import APIRouter

from suspark.suspark_modules_factory import ModulesFactory


def init_router(factory: ModulesFactory) -> APIRouter:
    router = APIRouter()

    @router.get("/modules", tags=["modules"])
    async def get_modules():
        return [{"username": "Rick"}, {"username": "Morty"}]

    return router
