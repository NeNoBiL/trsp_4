from itertools import count
from threading import Lock

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError

from app.validation import UserValidation
from app.exceptions import (
    CustomExceptionA,
    CustomExceptionB,
    custom_exception_a_handler,
    custom_exception_b_handler
)

app = FastAPI()

app.add_exception_handler(
    CustomExceptionA,
    custom_exception_a_handler
)

app.add_exception_handler(
    CustomExceptionB,
    custom_exception_b_handler
)

db = {}

_id_seq = count(start=1)
_lock = Lock()


def next_id():
    with _lock:
        return next(_id_seq)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors()
        }
    )


@app.get("/check-age/{age}")
def check_age(age: int):
    if age <= 18:
        raise CustomExceptionA()
    return {"message": "Возраст подходит"}


@app.get("/user/{user_id}")
def get_custom_user(user_id: int):
    if user_id not in db:
        raise CustomExceptionB()
    return db[user_id]


@app.post("/validate-user")
def validate_user(user: UserValidation):
    return {
        "message": "User valid",
        "data": user
    }


@app.post("/users", status_code=201)
def create_user(user: dict):
    user_id = next_id()
    db[user_id] = user
    return {
        "id": user_id,
        **user
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {
        "id": user_id,
        **db[user_id]
    }


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in db:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    del db[user_id]
    return Response(status_code=204)