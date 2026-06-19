import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every incoming HTTP request with method, path, status, and duration."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        method = request.method
        path = request.url.path
        query = request.url.query

        # Log the incoming request
        if query:
            logger.info("--> %s %s?%s", method, path, query)
        else:
            logger.info("--> %s %s", method, path)

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.error(
                "<-- %s %s — 500 Internal Server Error (%.0fms): %s",
                method, path, elapsed, exc,
            )
            raise

        elapsed = (time.perf_counter() - start_time) * 1000
        logger.info(
            "<-- %s %s — %d (%.0fms)",
            method, path, response.status_code, elapsed,
        )

        return response
