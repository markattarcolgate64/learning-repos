"""
Middleware Pipeline - Solution

A composable middleware pipeline similar to Express.js or Django middleware.
Each middleware receives a Request and a next_fn callback, and can inspect/modify
the request, call the next layer, and inspect/modify the response.
"""

from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class Request:
    """An HTTP-like request object flowing through the middleware pipeline.

    Attributes:
        path: The URL path (e.g. '/api/users').
        method: The HTTP method (e.g. 'GET', 'POST').
        headers: A dict of header name -> value pairs.
        body: The request body (any type).
        context: A dict for middleware to attach arbitrary data that
            downstream middleware or the handler can read.
    """

    path: str
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    body: Any = None
    context: dict = field(default_factory=dict)


@dataclass
class Response:
    """An HTTP-like response object returned by the handler or middleware.

    Attributes:
        status_code: The HTTP status code (e.g. 200, 404).
        headers: A dict of response header name -> value pairs.
        body: The response body (any type).
    """

    status_code: int = 200
    headers: dict = field(default_factory=dict)
    body: Any = None


class MiddlewarePipeline:
    """A composable middleware pipeline.

    Middleware functions are added with use() and executed in order. The
    final handler is set with set_handler(). Calling execute() runs the
    full chain: each middleware wraps the next, with the handler at the
    innermost layer.

    Middleware signature::

        def my_middleware(request: Request, next_fn: Callable) -> Response:
            # optionally modify request
            response = next_fn(request)
            # optionally modify response
            return response

    Handler signature::

        def my_handler(request: Request) -> Response:
            return Response(body="Hello")
    """

    def __init__(self) -> None:
        """Initialise the pipeline with an empty middleware list and no
        handler.
        """
        self._middlewares = []
        self._handler = None

    def use(self, middleware: Callable) -> "MiddlewarePipeline":
        """Add a middleware function to the pipeline.

        Middleware is executed in the order it is added.

        Args:
            middleware: A callable with signature
                (request: Request, next_fn: Callable) -> Response.

        Returns:
            self, to allow fluent chaining (e.g. pipeline.use(a).use(b)).
        """
        self._middlewares.append(middleware)
        return self

    def set_handler(self, handler: Callable) -> None:
        """Set the final request handler.

        Args:
            handler: A callable with signature
                (request: Request) -> Response.
        """
        self._handler = handler

    def execute(self, request: Request) -> Response:
        """Run the full middleware pipeline on a request.

        Builds the execution chain by wrapping the handler with each
        middleware in reverse order, then invokes the outermost layer.

        Args:
            request: The incoming Request to process.

        Returns:
            The final Response after all middleware and the handler have
            executed.

        Raises:
            RuntimeError: If no handler has been set.
        """
        if self._handler is None:
            raise RuntimeError("No handler has been set")

        current = self._handler
        for mw in reversed(self._middlewares):
            prev = current
            current = lambda req, _mw=mw, _next=prev: _mw(req, _next)

        return current(request)
