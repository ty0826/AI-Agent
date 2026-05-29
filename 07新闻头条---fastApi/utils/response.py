from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "success",
    code: int = 200,
    status_code: int = 200,
) -> JSONResponse:
    return api_response(
        code=code,
        message=message,
        data=data,
        status_code=status_code,
    )


def error_response(
    message: str,
    code: int,
    status_code: int,
    data: Any = None,
) -> JSONResponse:
    return api_response(
        code=code,
        message=message,
        data=data,
        status_code=status_code,
    )


def api_response(
    code: int,
    message: str,
    data: Any,
    status_code: int,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "code": code,
                "message": message,
                "data": data,
            }
        ),
    )
