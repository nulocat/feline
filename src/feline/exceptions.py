from feline.http.request import Request

class RouteLoadError(Exception):
    def __init__(self, message: str, path: str) -> None:
        full_message = f"{message} (path: {path})" if path else message
        super().__init__(full_message)

class OutOfScopeSupport(Exception):
    def __init__(self, message: str, current_scope: str) -> None:
        full_message = f"{message} (current scope: {current_scope})" if current_scope else message
        super().__init__(full_message)

class RouteHasNoResponse(Exception):
    def __init__(self, path: str, method: str, returned: object) -> None:
        super().__init__(
            f"The route '{path}' [{method}] returned an invalid response: "
            f"{repr(returned)} (type: {type(returned).__name__})"
        )

class RoutingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidParameterResolution(RoutingError):
    def __init__(
        self,
        request:Request,
        param: str,
        expected: str,
        given: str
    ) -> None:
        super().__init__(
            f"Invalid parameter received from IP {request.host} on route '{request.path}' [{request.method}]: "
            f"parameter '{param}' expected type '{expected}', but got '{given}'."
        )
