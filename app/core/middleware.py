from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.core.config import settings
from app.models.common.common_model import ErrorResponse

API_KEY = settings.API_KEY


def setup_origin_check(app: FastAPI):
    @app.middleware("http")
    async def check_origin(request: Request, call_next):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            error_response = ErrorResponse(
                status="error",
                description="Forbidden",
                data={"message": "Invalid or missing API key"}
            )
            return JSONResponse(status_code=403, content=error_response.dict())
        response = await call_next(request)
        return response
