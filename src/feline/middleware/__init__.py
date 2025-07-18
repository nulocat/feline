import asyncio
import inspect
from functools import wraps
from feline.http.response import Response
from feline.http.request import Request
from feline.context import context


class MidwareBase:
    def __init__(self) -> None:
        self.request: Request

    def __call__(self, func):
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs) -> Response:
                self.request = context.request

                before = self.before_request()
                if asyncio.iscoroutine(before):
                    before = await before
                if before is not None:
                    return before

                result = func(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    result = await result

                after = self.after_request(result)
                if asyncio.iscoroutine(after):
                    after = await after

                return after or result

            return async_wrapper

        else:

            @wraps(func)
            def wrapper(*args, **kwargs) -> Response:
                self.request = context.request

                before = self.before_request()
                if before is not None:
                    return before

                result = func(*args, **kwargs)
                after = self.after_request(result)

                return after or result

            return wrapper

    def before_request(self) -> Response | None:
        return None

    def after_request(self, response: Response) -> Response | None:
        return response
