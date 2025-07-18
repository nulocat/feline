import importlib
import importlib.util
import os
from types import FunctionType
from typing import Any, Callable

from feline.exceptions import RouteLoadError
from feline.routing.resolver import resolver_arguments


class Router:
    def __init__(self, routes_path="routes") -> None:
        self.routes: dict[str, dict[str, Callable]] = {}
        self.load_routes(routes_path)

    def _normalize_path(self, raw_path: str) -> str:
        path: str = raw_path.strip().lower()

        if path != "/" and path.endswith("/"):
            path = path[:-1]

        return path

    def set_route(self, method: str, path: str, function: FunctionType) -> None:
        uppered_method = method.upper()
        normalized_path = self._normalize_path(path)

        if method not in self.routes:
            self.routes[uppered_method] = {}

        self.routes[uppered_method][normalized_path] = function

    def load_routes(self, routes_path) -> None:
        for root, _, files in os.walk(routes_path):
            for file in files:
                if str(file).endswith(".py") and not str(file).startswith("_"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    relative_path = os.path.relpath(full_path, routes_path)

                    # Formata o caminho da URL
                    route_path = relative_path.replace(".py", "").replace("\\", "/")
                    if route_path.endswith("index"):
                        route_path = route_path[:-5]
                    url = "/" + route_path.strip("/")
                    url = self._normalize_path(url)

                    # Carrega o módulo
                    spec = importlib.util.spec_from_file_location(file, full_path)
                    if not spec or not spec.loader:
                        raise RouteLoadError("The path can't be loaded", path=full_path)

                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Registra as rotas GET e POST
                    if hasattr(module, "get"):
                        self.set_route("GET", url, module.get)

                    if hasattr(module, "post"):
                        self.set_route("POST", url, module.post)

                    if hasattr(module, "put"):
                        self.set_route("PUT", url, module.put)

                    if hasattr(module, "delete"):
                        self.set_route("DELETE", url, module.delete)

                    if hasattr(module, "patch"):
                        self.set_route("PATCH", url, module.patch)

    async def get_handler(
        self, method: str, path: str
    ) -> tuple[Callable, dict[str, Any]] | tuple[None, None]:
        """Retorna o handler (função) correspondente à rota."""
        fn = self.routes.get(method.upper(), {}).get(self._normalize_path(path))

        if fn is not None:
            arguments = await resolver_arguments(fn)
            return fn, arguments

        return None, None
