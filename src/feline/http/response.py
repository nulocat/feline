from typing import Self
from typing import Any
import json

from feline.http.cookies import Cookies
from feline.context import context


class Response:
    def __init__(self, content=b"", status_code=200, headers: dict | None = None):
        # Inicializando o corpo, status e headers
        self.content: bytes = content
        self.status_code: int = status_code
        self.headers: dict[str, str] = headers or {}

    def set_header(self, name, value) -> None:
        """Define um header para a resposta."""
        self.headers[name] = value

    def get_headers(self) -> list[tuple[bytes, bytes]]:
        headers: list[tuple[bytes, bytes]] = [
            (k.encode(encoding="latin1"), v.encode(encoding="latin1"))
            for k, v in self.headers.items()
        ]

        cookies: Cookies = context.cookies
        changed_cookies: list[tuple[bytes, bytes]] = (
            cookies.get_headers_of_cookie_to_set()
        )

        headers.extend(changed_cookies)
        headers.append((b"content-length", str(len(bytes(self))).encode()))

        return headers

    def json(self, data: dict) -> Self:
        """Retorna a resposta no formato JSON."""
        import json

        self.content = json.dumps(obj=data).encode(encoding="utf-8")
        self.set_header(name="Content-Type", value="application/json")
        return self

    def html(self, data: str) -> Self:
        """Retorna a resposta no formato HTML."""
        self.content = data.encode("utf-8")
        self.set_header(name="Content-Type", value="text/html")
        return self

    def text(self, data: str) -> Self:
        """Retorna a resposta no formato de texto simples."""
        self.content = data.encode("utf-8")
        self.set_header(name="Content-Type", value="text/plain")
        return self

    def __bytes__(self) -> bytes:
        """Quando for enviado, a resposta é transformada em bytes."""
        return self.content


def redirect(to: str, permanent: bool = False) -> Response:
    status_code = 301 if permanent else 302
    res = Response(status_code=status_code)
    res.set_header("Location", to)
    res.set_header("Content-Type", "text/plain")
    res.content = f"Redirecting to {to}".encode("utf-8")
    return res


def html(
    data: str, status: int = 200, headers: dict[str, str] | None = None
) -> Response:
    res = Response(status_code=status, headers=headers)
    res.set_header("Content-Type", "text/html")
    res.content = data.encode("utf-8")
    return res


def json_response(
    data: Any, status: int = 200, headers: dict[str, str] | None = None
) -> Response:
    res = Response(status_code=status, headers=headers)
    res.set_header("Content-Type", "application/json")
    res.content = json.dumps(data).encode("utf-8")
    return res


def text(
    data: str, status: int = 200, headers: dict[str, str] | None = None
) -> Response:
    res = Response(status_code=status, headers=headers)
    res.set_header("Content-Type", "text/plain")
    res.content = data.encode("utf-8")
    return res


def bad_request(message: str = "Bad Request") -> Response:
    return text(message, status=400)


def not_found(message: str = "Not Found") -> Response:
    return text(message, status=404)


def unauthorized(message: str = "Unauthorized") -> Response:
    return text(message, status=401)


def server_error(message: str = "Internal Server Error") -> Response:
    return text(message, status=500)
