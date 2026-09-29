import time
import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("device_systems")
logging.basicConfig(level=logging.INFO)


class RequestMiddleware(BaseHTTPMiddleware):
    """Middleware personalizado: mide tiempo de respuesta, agrega cabeceras
    de trazabilidad (X-Process-Time, X-App-Name, X-Request-ID) y registra
    método, ruta y código de estado de cada petición."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        # Propaga el X-Request-ID si el cliente ya envió uno, o genera uno nuevo
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "%s %s - status=%s - time=%.4fs - request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
            request_id,
        )

        return response