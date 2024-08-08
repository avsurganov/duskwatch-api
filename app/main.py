from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.api import api_router
from app.core.middleware import setup_origin_check
from app.utils.exception_handlers import http_exception_handler, generic_exception_handler, \
    validation_exception_handler, starlette_http_exception_handler

app = FastAPI(
    title="Duskwatch API",
    description="This is a backend API for the tool Duskwatch",
    version="1.0.0",
    contact={
        "name": "Surganov Dev",
        "email": "info@surganov.dev",
    }
)

setup_origin_check(app)

app.include_router(api_router, prefix="/api")

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
