from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import DeployHubException


def deployhub_exception_handler(
    request: Request, exc: DeployHubException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers,
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(DeployHubException, deployhub_exception_handler)  # type: ignore
