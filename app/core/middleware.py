from fastapi import FastAPI, Request, HTTPException

from app.core.config import settings

API_KEY = settings.API_KEY


def setup_origin_check(app: FastAPI):
    @app.middleware("http")
    async def check_origin(request: Request, call_next):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            raise HTTPException(status_code=403, detail="Forbidden")
        response = await call_next(request)
        return response
