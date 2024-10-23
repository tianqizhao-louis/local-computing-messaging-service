from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pet-service")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log before the request is processed
        logger.info(f"Request started: {request.method} {request.url}")

        # Log query parameters (for debugging purposes)
        logger.info(f"Query parameters: {request.query_params}")

        start_time = time.time()

        # Call the next middleware or route handler
        response = await call_next(request)

        # Log after the response is generated
        process_time = time.time() - start_time
        logger.info(
            f"Request completed in {process_time:.4f} seconds with status code {response.status_code}"
        )

        return response
