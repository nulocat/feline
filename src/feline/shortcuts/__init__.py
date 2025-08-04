from feline.application import Feline as App
from feline.config import Config
from feline.context import context as _context
from feline.extensions.utils.render import render
from feline.http.cookies import Cookies
from feline.http.request import Request
from feline.http.response import (Response, html, json_response, not_found,
                                  redirect, server_error, text, unauthorized)


def get_cookies() -> Cookies:
    return _context.cookies


def get_request() -> Request:
    return _context.request


def get_response() -> Response:
    return _context.response


def get_config() -> Config:
    return _context.config
