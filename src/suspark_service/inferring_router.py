from typing import Any, Callable, List, get_type_hints

import pydantic
from fastapi import APIRouter


class InferringRouter(APIRouter):
    """
    Overrides the route decorator logic to use the annotated return type as the `response_model` if unspecified.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> Any:
        if kwargs.get("response_model") is None:
            return_type: Any = get_type_hints(endpoint).get("return")
            if issubclass(return_type, (pydantic.BaseModel, List)):
                kwargs["response_model"] = get_type_hints(endpoint).get("return")
        return super().add_api_route(path, endpoint, **kwargs)
