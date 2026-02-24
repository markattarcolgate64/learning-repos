"""
Tests for Middleware Pipeline.

Run with:
    python -m unittest 12_middleware_pipeline.test_exercise -v
"""

import unittest
from .exercise import MiddlewarePipeline, Request, Response


class TestMiddlewarePipeline(unittest.TestCase):
    """Comprehensive tests for the middleware pipeline."""

    # ------------------------------------------------------------------
    # 1. No middleware: request goes straight to handler
    # ------------------------------------------------------------------

    def test_no_middleware(self):
        """Without middleware, the handler should receive the request directly."""
        pipeline = MiddlewarePipeline()
        pipeline.set_handler(lambda req: Response(status_code=200, body=f"path={req.path}"))

        resp = pipeline.execute(Request(path="/hello"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "path=/hello")

    # ------------------------------------------------------------------
    # 2. Single middleware: modifies request before handler
    # ------------------------------------------------------------------

    def test_single_middleware_modifies_request(self):
        """A single middleware should be able to modify the request before the handler."""
        def uppercase_path(request, next_fn):
            request.path = request.path.upper()
            return next_fn(request)

        pipeline = MiddlewarePipeline()
        pipeline.use(uppercase_path)
        pipeline.set_handler(lambda req: Response(body=req.path))

        resp = pipeline.execute(Request(path="/hello"))
        self.assertEqual(resp.body, "/HELLO")

    # ------------------------------------------------------------------
    # 3. Middleware ordering: runs in added order
    # ------------------------------------------------------------------

    def test_middleware_ordering(self):
        """Middleware should execute in the order they were added."""
        call_order = []

        def mw_a(request, next_fn):
            call_order.append("A")
            return next_fn(request)

        def mw_b(request, next_fn):
            call_order.append("B")
            return next_fn(request)

        def mw_c(request, next_fn):
            call_order.append("C")
            return next_fn(request)

        pipeline = MiddlewarePipeline()
        pipeline.use(mw_a)
        pipeline.use(mw_b)
        pipeline.use(mw_c)
        pipeline.set_handler(lambda req: Response(body="done"))

        pipeline.execute(Request(path="/test"))
        self.assertEqual(call_order, ["A", "B", "C"])

    # ------------------------------------------------------------------
    # 4. Short-circuit: middleware returns Response without calling next
    # ------------------------------------------------------------------

    def test_short_circuit(self):
        """A middleware can short-circuit by returning a Response without calling next_fn."""
        handler_called = {"value": False}

        def auth_middleware(request, next_fn):
            if request.headers.get("Authorization") is None:
                return Response(status_code=401, body="Unauthorized")
            return next_fn(request)

        def handler(request):
            handler_called["value"] = True
            return Response(body="OK")

        pipeline = MiddlewarePipeline()
        pipeline.use(auth_middleware)
        pipeline.set_handler(handler)

        # No auth header -> short-circuit
        resp = pipeline.execute(Request(path="/secret"))
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.body, "Unauthorized")
        self.assertFalse(handler_called["value"],
                         "Handler should not have been called on short-circuit.")

    # ------------------------------------------------------------------
    # 5. Post-processing: middleware modifies response after handler
    # ------------------------------------------------------------------

    def test_post_processing(self):
        """Middleware should be able to modify the response after calling next_fn."""
        def add_header_mw(request, next_fn):
            response = next_fn(request)
            response.headers["X-Processed"] = "true"
            return response

        pipeline = MiddlewarePipeline()
        pipeline.use(add_header_mw)
        pipeline.set_handler(lambda req: Response(body="data"))

        resp = pipeline.execute(Request(path="/"))
        self.assertEqual(resp.headers["X-Processed"], "true")
        self.assertEqual(resp.body, "data")

    # ------------------------------------------------------------------
    # 6. Context passing: middleware writes to request.context, handler reads it
    # ------------------------------------------------------------------

    def test_context_passing(self):
        """Middleware can write to request.context and the handler can read it."""
        def inject_user(request, next_fn):
            request.context["user"] = "alice"
            return next_fn(request)

        def handler(request):
            user = request.context.get("user", "anonymous")
            return Response(body=f"Hello, {user}!")

        pipeline = MiddlewarePipeline()
        pipeline.use(inject_user)
        pipeline.set_handler(handler)

        resp = pipeline.execute(Request(path="/"))
        self.assertEqual(resp.body, "Hello, alice!")

    # ------------------------------------------------------------------
    # 7. use() returns self for chaining
    # ------------------------------------------------------------------

    def test_use_returns_self(self):
        """use() should return the pipeline instance for fluent chaining."""
        pipeline = MiddlewarePipeline()
        result = pipeline.use(lambda req, next_fn: next_fn(req))
        self.assertIs(result, pipeline)

        # Verify chaining works
        pipeline.use(lambda req, nxt: nxt(req)).use(lambda req, nxt: nxt(req))
        pipeline.set_handler(lambda req: Response(body="chained"))
        resp = pipeline.execute(Request(path="/"))
        self.assertEqual(resp.body, "chained")

    # ------------------------------------------------------------------
    # 8. No handler raises RuntimeError
    # ------------------------------------------------------------------

    def test_no_handler_raises(self):
        """execute() without a handler set should raise RuntimeError."""
        pipeline = MiddlewarePipeline()
        with self.assertRaises(RuntimeError):
            pipeline.execute(Request(path="/"))

    # ------------------------------------------------------------------
    # 9. Multiple middleware: logging -> auth -> handler pipeline
    # ------------------------------------------------------------------

    def test_logging_auth_handler_pipeline(self):
        """A realistic pipeline with logging and auth middleware."""
        log = []

        def logging_mw(request, next_fn):
            log.append(f"REQUEST {request.method} {request.path}")
            response = next_fn(request)
            log.append(f"RESPONSE {response.status_code}")
            return response

        def auth_mw(request, next_fn):
            token = request.headers.get("Authorization")
            if token == "Bearer valid-token":
                request.context["authenticated"] = True
                return next_fn(request)
            return Response(status_code=403, body="Forbidden")

        def handler(request):
            if request.context.get("authenticated"):
                return Response(status_code=200, body="Secret data")
            return Response(status_code=403, body="Forbidden")

        pipeline = MiddlewarePipeline()
        pipeline.use(logging_mw).use(auth_mw)
        pipeline.set_handler(handler)

        # Authorized request
        req = Request(path="/api/data", headers={"Authorization": "Bearer valid-token"})
        resp = pipeline.execute(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, "Secret data")
        self.assertIn("REQUEST GET /api/data", log)
        self.assertIn("RESPONSE 200", log)

        # Unauthorized request
        log.clear()
        req2 = Request(path="/api/data")
        resp2 = pipeline.execute(req2)
        self.assertEqual(resp2.status_code, 403)
        self.assertIn("REQUEST GET /api/data", log)
        self.assertIn("RESPONSE 403", log)

    # ------------------------------------------------------------------
    # 10. Middleware can modify response headers
    # ------------------------------------------------------------------

    def test_middleware_modifies_response_headers(self):
        """Multiple middleware layers can each add or modify response headers."""
        def cors_mw(request, next_fn):
            response = next_fn(request)
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response

        def cache_mw(request, next_fn):
            response = next_fn(request)
            response.headers["Cache-Control"] = "no-store"
            return response

        pipeline = MiddlewarePipeline()
        pipeline.use(cors_mw)
        pipeline.use(cache_mw)
        pipeline.set_handler(lambda req: Response(body="response"))

        resp = pipeline.execute(Request(path="/"))
        self.assertEqual(resp.headers["Access-Control-Allow-Origin"], "*")
        self.assertEqual(resp.headers["Cache-Control"], "no-store")
        self.assertEqual(resp.body, "response")


if __name__ == "__main__":
    unittest.main()
