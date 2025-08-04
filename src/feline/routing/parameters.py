from typing import Generic, Literal, Optional, TypeVar

T = TypeVar("T")


class Query(Generic[T]):
    def __init__(self, default: Optional[T] = None):
        self.default: Optional[T] = default

    def __repr__(self):
        return f"Query(default={self.default!r})"


class Form(Generic[T]):
    def __init__(self, default: Optional[T] = None):
        self.default: Optional[T] = default

    def __repr__(self):
        return f"Form(default={self.default!r})"


class Body(Generic[T]):
    def __init__(
        self, default: Optional[T] = None, type: Literal["JSON", "TEXT"] = "JSON"
    ):
        self.default: Optional[T] = default
        self.type = type

    def __repr__(self):
        return f"Body(default={self.default!r}, type={self.type!r})"
