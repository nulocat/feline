import importlib
from typing import Callable
import uvicorn

from feline.config import Config
from feline.context import _Context, context
from feline.context.manager import request_context_window
from feline.exceptions import OutOfScopeSupport, RouteHasNoResponse
from feline.http.request import Request
from feline.http.response import Response, not_found
from feline.routing.router import Router
from rich.traceback import install as rich_trace_install
import inspect


rich_trace_install()


# === App Class ===
class Feline:
    def __init__(
        self, config: Config = Config(), shutdown_callback: Callable | None = None
    ) -> None:
        self.context: _Context = context

        self.context.config = config
        self.config: Config = self.context.config

        self.router = Router(routes_path=config.routes_path)

        self.exception_handles = []

        self.shutdown_callback = shutdown_callback

    async def handle_request(self) -> Response:
        """Resolve a rota e chama o handler correspondente."""
        request: Request = context.request

        method: str = request.method.upper()
        path: str = request.path.lower()

        handler, arguments = await self.router.get_handler(method, path)

        if handler is None or arguments is None:
            return not_found()

        if inspect.iscoroutinefunction(handler):
            response = await handler(**arguments)
        else:
            response = handler(**arguments)

        if response is None:
            raise RouteHasNoResponse(path, method, response)

        elif isinstance(response, str) and "<html>" in response:
            response: Response = Response().html(response)

        elif isinstance(response, dict):
            response: Response = Response().json(response)

        elif not isinstance(response, Response):
            response: Response = Response().text(str(response))

        return response

    async def handle_lifespan(self, scope, receive, send):
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                # app init (nothing for now)
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                # app save kill (nothing for now)
                if isinstance(self.shutdown_callback, Callable):
                    self.shutdown_callback()
                await send({"type": "lifespan.shutdown.complete"})
                return

    # the uvicorn call
    async def __call__(self, scope, receive, send):
        try:
            if scope["type"] == "http":
                async with request_context_window(scope, receive) as window:

                    response: Response = await self.handle_request()

                    await send(
                        {
                            "type": "http.response.start",
                            "status": response.status_code,
                            "headers": response.get_headers(),
                        }
                    )
                    await send(
                        {
                            "type": "http.response.body",
                            "body": bytes(response),
                            "more_body": False,
                        }
                    )
            elif scope["type"] == "lifespan":
                await self.handle_lifespan(scope=scope, receive=receive, send=send)
            else:
                raise OutOfScopeSupport(
                    message="ERR: Out of scope support (only: http, lifespan) ",
                    current_scope=scope[type],
                )
        except Exception as e:
            for exception_type, handle_function in self.exception_handles:
                if isinstance(e, exception_type):
                    return handle_function()
            raise e  # TEMP, future handle erro

    def run(self, import_path: str, host="127.0.0.1", port=5000, debug=False) -> None:

        if ":" not in import_path:
            import_path = import_path + ":app"

        module_name, app_name = import_path.split(":")
        print(import_path)

        try:
            mod = importlib.import_module(module_name)
            app = getattr(mod, app_name)

            if not debug:
                uvicorn.run(app, host=host, port=port, reload=debug)
            else:
                uvicorn.run(import_path, host=host, port=port, reload=True)
        except ModuleNotFoundError as e:
            print(f"❌ Módulo não encontrado: {e.name}")
            return
        except AttributeError:
            print(f"❌ O objeto '{app_name}' não existe no módulo '{module_name}'")
            return
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return
        print(f"🚀 Rodando {import_path} em http://{host}:{port} ...")

    def get(self, path) -> Callable:
        def decorator(func) -> Callable:
            self.router.set_route("GET", path, func)
            return func

        return decorator

    def post(self, path) -> Callable:
        def decorator(func) -> Callable:
            self.router.set_route("POST", path, func)
            return func

        return decorator

    def onerror(self, exception=Exception) -> Callable:
        def decorator(func) -> Callable:
            self.exception_handles.append((exception, func))
            return func

        return decorator
