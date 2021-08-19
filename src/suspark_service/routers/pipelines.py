from fastapi import APIRouter


def init_router() -> APIRouter:
    router = APIRouter()

    @router.get("/users/", tags=["users"])
    async def read_users():
        return [{"username": "Rick"}, {"username": "Morty"}]

    return router
