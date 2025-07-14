from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, cast

from feline.config import Config
from feline.structures import AttributeDict

if TYPE_CHECKING:
    from feline.http.request import Request
    from feline.http.response import Response

    from feline.http.cookies import Cookies

class GlobalObject(AttributeDict):
    def __init__(self):
        super().__init__()

_ctx_cookies: ContextVar[Cookies] = ContextVar("cookies")
_ctx_request: ContextVar[Request] = ContextVar("request")
_ctx_response: ContextVar[Response] = ContextVar("response")
_ctx_config: ContextVar[Config] = ContextVar("config")
_ctx_global: ContextVar[GlobalObject] = ContextVar("global")
_ctx_global.set(GlobalObject())


class _Context:
    @property
    def cookies(self) -> Cookies:
        return cast("Cookies", _ctx_cookies.get())
    
    @cookies.setter
    def cookies(self, value: Cookies) -> None:
        _ctx_cookies.set(value)

    @property
    def request(self) -> Request:
        return cast("Request", _ctx_request.get())

    @request.setter
    def request(self, value: Request) -> None:
        _ctx_request.set(value)

    @property
    def response(self) -> Response:
        return cast("Response", _ctx_response.get())

    @response.setter
    def response(self, value: Response) -> None:
        _ctx_response.set(value)

    @property
    def config(self) -> Config:
        return _ctx_config.get()

    @config.setter
    def config(self, value: Config) -> None:
        _ctx_config.set(value)

    @property
    def g(self) -> GlobalObject:
        return _ctx_global.get()


context = _Context()


