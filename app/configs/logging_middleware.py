from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from app.configs.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async  def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = round((time.time() - start_time) * 1000)

        logger.bind(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=duration,
            client_ip=request.client.host
        ).info("Request processed")

        return response