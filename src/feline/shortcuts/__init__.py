from feline.application import Feline as App
from feline.config import Config
from feline.context import context as _context
from feline.http.request import Request
from feline.http.cookies import Cookies
from feline.http.response import (
    Response,
    html,
    json_response,
    not_found,
    redirect,
    server_error,
    text,
    unauthorized,
)

from feline.extensions.utils.render import render


def cookies() -> Cookies:
    return _context.cookies


def request() -> Request:
    return _context.request


def response() -> Response:
    return _context.response


def config() -> Config:
    return _context.config
