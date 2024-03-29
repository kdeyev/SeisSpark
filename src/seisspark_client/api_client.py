# =============================================================================
# Copyright (c) 2021 SeisSpark (https://github.com/kdeyev/SeisSpark).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from asyncio import get_event_loop
from typing import Any, Awaitable, Callable, Dict, Generic, Optional, Type, TypeVar, overload

from httpx import AsyncClient, Request, Response
from pydantic import ValidationError, parse_obj_as

from seisspark_client.api.modules_api import AsyncModulesApi, SyncModulesApi
from seisspark_client.api.pipelines_api import AsyncPipelinesApi, SyncPipelinesApi
from seisspark_client.exceptions import ResponseHandlingException, UnexpectedResponse

ClientT = TypeVar("ClientT", bound="ApiClient")


class AsyncApis(Generic[ClientT]):
    def __init__(self, client: ClientT):
        self.client = client

        self.modules_api = AsyncModulesApi(self.client)
        self.pipelines_api = AsyncPipelinesApi(self.client)


class SyncApis(Generic[ClientT]):
    def __init__(self, client: ClientT):
        self.client = client

        self.modules_api = SyncModulesApi(self.client)
        self.pipelines_api = SyncPipelinesApi(self.client)


T = TypeVar("T")
Send = Callable[[Request], Awaitable[Response]]
MiddlewareT = Callable[[Request, Send], Awaitable[Response]]


class ApiClient:
    def __init__(self, host: Optional[str] = None, **kwargs: Any) -> None:
        self.host = host
        self.middleware: MiddlewareT = BaseMiddleware()
        self._async_client = AsyncClient(**kwargs)

    @overload
    async def request(self, *, type_: Type[T], method: str, url: str, path_params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> T:
        ...

    @overload  # noqa F811
    async def request(self, *, type_: None, method: str, url: str, path_params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> None:
        ...

    async def request(self, *, type_: Any, method: str, url: str, path_params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:  # noqa F811
        if path_params is None:
            path_params = {}
        url = (self.host or "") + url.format(**path_params)
        request = Request(method, url, **kwargs)
        return await self.send(request, type_)

    @overload
    def request_sync(self, *, type_: Type[T], **kwargs: Any) -> T:
        ...

    @overload  # noqa F811
    def request_sync(self, *, type_: None, **kwargs: Any) -> None:
        ...

    def request_sync(self, *, type_: Any, **kwargs: Any) -> Any:  # noqa F811
        """
        This method is not used by the generated apis, but is included for convenience
        """
        return get_event_loop().run_until_complete(self.request(type_=type_, **kwargs))

    async def send(self, request: Request, type_: Type[T]) -> T:
        response = await self.middleware(request, self.send_inner)
        if response.status_code in [200, 201]:
            try:
                if type_ is None:
                    return None  # type: ignore
                return parse_obj_as(type_, response.json())
            except ValidationError as e:
                raise ResponseHandlingException(e)
        raise UnexpectedResponse.for_response(response)

    async def send_inner(self, request: Request) -> Response:
        try:
            response = await self._async_client.send(request)
        except Exception as e:
            raise ResponseHandlingException(e)
        return response

    def add_middleware(self, middleware: MiddlewareT) -> None:
        current_middleware = self.middleware

        async def new_middleware(request: Request, call_next: Send) -> Response:
            async def inner_send(request: Request) -> Response:
                return await current_middleware(request, call_next)

            return await middleware(request, inner_send)

        self.middleware = new_middleware


class BaseMiddleware:
    async def __call__(self, request: Request, call_next: Send) -> Response:
        return await call_next(request)
