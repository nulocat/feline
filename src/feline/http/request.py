from typing import Any, Awaitable, Callable
from urllib.parse import parse_qs

from asgiref.typing import HTTPScope

from feline.structures import AttributeDict

Receive = Callable[[], Awaitable[dict[str, bytes | bool]]]


class Request:
    def __init__(self, scope: HTTPScope, receive: Receive) -> None:
        self.scope: HTTPScope = scope
        self._receive: Receive = receive
        self.host, self.port = scope["client"] or ("Unknow",0)
        self.method: str = scope["method"]
        self.path: str = scope["path"]
        self._cached_body: bytes | None = None
        self._cached_form: dict[str, str] | None = None
        self._cached_json: dict[str, Any] | None = None
        self._cached_text: str | None = None
        self._cached_args: dict[str, str] | None = None

        self.headers: dict[str, str] = {
            k.decode(encoding="latin1").lower(): v.decode(encoding="latin1")
            for k, v in scope.get("headers", [])
        }

        self.metadata = AttributeDict()

    def _parse_query_params(self, query_string: bytes) -> dict[str, str]:
        # Faz parsing e converte listas para valores únicos
        parsed = parse_qs(query_string.decode("utf-8"))
        return {k: v[0] for k, v in parsed.items()}

    @property
    async def body(self) -> bytes:
        """Read and return the body of the request."""

        if self._cached_body is None:

            body: bytes = b""
            more_body: bool = True

            while more_body:
                message: dict[str, bytes | bool] = await self._receive()
                body += bytes(message.get("body", b""))
                more_body = bool(message.get("more_body", False))

            self._cached_body = body
            return body
        return self._cached_body

    @property
    async def json(self) -> dict[str, Any]:
        """Parse the request body as JSON."""
        if self._cached_json is None:
            import json

            self._cached_json = json.loads(s=bytes(await self.body).decode(encoding="utf-8"))
        return self._cached_json or {}
    
    @property
    async def form(self) -> dict[str, str]:
        """Parse the request body as form data."""
        if self._cached_form is None:
            self._cached_form = self._parse_query_params(query_string=bytes(await self.body))
        
        return self._cached_form
    
    @property
    async def text(self) -> str:
        if self._cached_text is None:
            self._cached_text = str(bytes(await self.body).decode())
        return self._cached_text
    
    @property
    def args(self) -> dict[str, str]:
        if self._cached_args is None:
            self._cached_args = self._parse_query_params(query_string=self.scope["query_string"]) 
        return self._cached_args

