from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    status_code: int


class CustomExceptionA(Exception):
    def __init__(self):
        self.message = "Возраст должен быть больше 18"
        self.status_code = 400


class CustomExceptionB(Exception):
    def __init__(self):
        self.message = "Пользователь не найден"
        self.status_code = 404


async def custom_exception_a_handler(
        request: Request,
        exc: CustomExceptionA
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "status_code": exc.status_code
        }
    )


async def custom_exception_b_handler(
        request: Request,
        exc: CustomExceptionB
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "status_code": exc.status_code
        }
    )