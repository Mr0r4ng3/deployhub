from fastapi import status
from typing import Literal
from pydantic import BaseModel, Field, create_model


class DeployHubException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers

    @classmethod
    def schema(cls) -> type[BaseModel]:
        error_literal = Literal[cls.__name__]  # type: ignore

        return create_model(
            cls.__name__,
            error=(error_literal, Field(examples=[cls.__name__])),
            detail=(str, ...),
        )


class InvalidCredentials(DeployHubException):
    def __init__(
        self,
        message: str = "Invalid credentials",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)


class NotAuthenticated(DeployHubException):
    def __init__(
        self,
        message: str = "Not authenticated",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)


class ResourceNotFound(DeployHubException):
    def __init__(
        self,
        message: str = "Resource not found",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message, status_code)
