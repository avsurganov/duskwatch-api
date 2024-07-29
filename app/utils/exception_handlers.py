from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.common.common_model import ErrorResponse
from app.models.common.common_responses import common_responses


async def http_exception_handler(request: Request, exc: HTTPException):
    description = common_responses.get(exc.status_code, {}).get("description", "HTTP Error")
    response_data = ErrorResponse(
        status="error",
        data={"message": exc.detail},
        description=description
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data.dict()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    description = common_responses.get(422, {}).get("description", "Validation Error")
    response_data = ErrorResponse(
        status="error",
        data={"message": exc.errors()},
        description=description
    )
    return JSONResponse(
        status_code=422,
        content=response_data.dict()
    )


async def generic_exception_handler(request: Request, exc: Exception):
    description = common_responses.get(500, {}).get("description", "Internal Server Error")
    response_data = ErrorResponse(
        status="error",
        data={"message": str(exc)},
        description=description
    )
    return JSONResponse(
        status_code=500,
        content=response_data.dict()
    )
