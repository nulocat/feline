from secrets import token_urlsafe
from typing import Any


class Config:
    def __init__(self):
        self.__dict__["debug"] = False
        self.__dict__["secret_key"] = token_urlsafe(nbytes=32)
        self.__dict__["routes_path"] = "routes"
        self.__dict__["templates_path"] = "templates"

    def __getattr__(self, name: str) -> Any:
        return self.__dict__.get(name, None)

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value


