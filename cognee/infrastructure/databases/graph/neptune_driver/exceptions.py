"""Neptune DB Exceptions

This module defines custom exceptions for Neptune DB operations.
"""

from cognee.exceptions import CogneeApiError
from fastapi import status


class NeptuneDBError(CogneeApiError):
    """Base exception for Neptune DB operations."""

    def __init__(
        self,
        message: str = "Neptune DB error.",
        name: str = "NeptuneDBError",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBConnectionError(NeptuneDBError):
    """Exception raised when connection to Neptune DB fails."""

    def __init__(
        self,
        message: str = "Unable to connect to Neptune DB. Please check the endpoint and network connectivity.",
        name: str = "NeptuneDBConnectionError",
        status_code=status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBQueryError(NeptuneDBError):
    """Exception raised when a query execution fails."""

    def __init__(
        self,
        message: str = "The query execution failed due to invalid syntax or semantic issues.",
        name: str = "NeptuneDBQueryError",
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBAuthenticationError(NeptuneDBError):
    """Exception raised when authentication with Neptune DB fails."""

    def __init__(
        self,
        message: str = "Authentication with Neptune DB failed. Please verify your credentials.",
        name: str = "NeptuneDBAuthenticationError",
        status_code=status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBConfigurationError(NeptuneDBError):
    """Exception raised when Neptune DB configuration is invalid."""

    def __init__(
        self,
        message: str = "Neptune DB configuration is invalid or incomplete. Please review your setup.",
        name: str = "NeptuneDBConfigurationError",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBTimeoutError(NeptuneDBError):
    """Exception raised when a Neptune DB operation times out."""

    def __init__(
        self,
        message: str = "The operation timed out while communicating with Neptune DB.",
        name: str = "NeptuneDBTimeoutError",
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBThrottlingError(NeptuneDBError):
    """Exception raised when requests are throttled by Neptune DB."""

    def __init__(
        self,
        message: str = "Request was throttled by Neptune DB due to exceeding rate limits.",
        name: str = "NeptuneDBThrottlingError",
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBResourceNotFoundError(NeptuneDBError):
    """Exception raised when a Neptune DB resource is not found."""

    def __init__(
        self,
        message: str = "The requested Neptune DB resource could not be found.",
        name: str = "NeptuneDBResourceNotFoundError",
        status_code=status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(message, name, status_code)


class NeptuneDBInvalidParameterError(NeptuneDBError):
    """Exception raised when invalid parameters are provided to Neptune DB."""

    def __init__(
        self,
        message: str = "One or more parameters provided to Neptune DB are invalid or missing.",
        name: str = "NeptuneDBInvalidParameterError",
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, name, status_code)
