from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.response import error_response


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)


async def http_exception_handler(request: Request, exc: HTTPException | StarletteHTTPException):
    message = exc.detail if isinstance(exc.detail, str) else _status_message(exc.status_code)
    return error_response(
        code=exc.status_code,
        message=message,
        data=None,
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(
        code=422,
        message="Validation error",
        data=exc.errors(),
        status_code=422,
    )


async def value_error_handler(request: Request, exc: ValueError):
    return error_response(
        code=400,
        message=str(exc) or "Bad request",
        data=None,
        status_code=400,
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return error_response(
        code=500,
        message="Database error",
        data=None,
        status_code=500,
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    return error_response(
        code=500,
        message="Internal server error",
        data=None,
        status_code=500,
    )


def _status_message(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Request failed"
