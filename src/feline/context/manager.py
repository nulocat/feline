from contextlib import asynccontextmanager

from feline.context import context
from feline.http.cookies import Cookies
from feline.http.request import Request


@asynccontextmanager
async def request_context_window(scope, receive):
    req = Request(scope, receive)
    context.request = req

    cookie_header = dict(scope["headers"]).get(b"cookie", b"").decode("latin1")
    context.cookies = Cookies(cookie_header)

    yield
