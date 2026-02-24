"""
Middleware Pipeline
===================
Category   : Full-Stack / Systems
Difficulty : ** (2/5)

Problem
-------
Implement a middleware pipeline similar to those found in Express.js and
Django.  Each middleware function receives a Request and a next_fn callback.
It can:

1. Inspect or modify the Request before passing it along.
2. Call next_fn(request) to invoke the next middleware (or the final handler).
3. Inspect or modify the Response returned by next_fn before passing it back.
4. Short-circuit the pipeline by returning a Response directly without
   calling next_fn.

The pipeline ends with a final handler that produces the initial Response.

Real-world motivation
---------------------
Middleware pipelines are a ubiquitous pattern in web frameworks:
  - Express.js uses app.use(middleware) for logging, auth, CORS, etc.
  - Django's MIDDLEWARE setting chains request/response processors.
  - FastAPI and Flask have similar before/after request hooks.

This pattern cleanly separates cross-cutting concerns (authentication,
logging, rate limiting) from business logic.  Understanding how to build
the chain from scratch deepens your knowledge of function composition and
the decorator pattern.

Hints
-----
1. Build the chain from the inside out: start with the final handler and
   wrap each middleware around it in reverse order.
2. Each layer creates a closure: lambda req: middleware(req, next_layer).
3. use() should return self so middleware can be chained fluently:
   pipeline.use(mw_a).use(mw_b).set_handler(handler)
4. A middleware that does NOT call next_fn short-circuits -- the rest of
   the pipeline (and the handler) never execute.

Run command
-----------
    pytest 12_middleware_pipeline/test_exercise.py -v
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

    Middleware functions are added with use() and executed in order.  The
    final handler is set with set_handler().  Calling execute() runs the
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
        # TODO: Create an empty list for middleware functions.
        # TODO: Set the handler to None.
        pass

    def use(self, middleware: Callable) -> "MiddlewarePipeline":
        """Add a middleware function to the pipeline.

        Middleware is executed in the order it is added.

        Args:
            middleware: A callable with signature
                (request: Request, next_fn: Callable) -> Response.

        Returns:
            self, to allow fluent chaining (e.g. pipeline.use(a).use(b)).
        """
        # TODO: Append the middleware to the list.
        # TODO: Return self for chaining.
        pass

    def set_handler(self, handler: Callable) -> None:
        """Set the final request handler.

        The handler is the innermost function in the pipeline.  It receives
        the (possibly modified) Request and must return a Response.

        Args:
            handler: A callable with signature
                (request: Request) -> Response.
        """
        # TODO: Store the handler.
        pass

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
        # TODO: Raise RuntimeError if self._handler is None.
        # TODO: Start with current = self._handler.
        # TODO: Iterate over middleware in reverse order.  For each
        #       middleware, wrap current in a new function that calls
        #       middleware(request, current).
        # TODO: Call the outermost function with the request and return
        #       the Response.
        # Hint: Build from innermost outward:
        #       for mw in reversed(self._middlewares):
        #           prev = current
        #           current = lambda req, _mw=mw, _next=prev: _mw(req, _next)
        #       return current(request)
        pass
