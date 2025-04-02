from typing import Final
from uuid import UUID

from fastapi import Request

from blog.application.common.application_error import ApplicationError, ErrorType
from blog.application.ports.identity_provider import IdentityProvider
from blog.domain.shared.user_id import UserId


class HttpIdentityProvider(IdentityProvider):
    _USER_ROLE_HEADER: Final[str] = "X-Auth-User-Role"
    _USER_ID_HEADER: Final[str] = "X-Auth-User-Id"

    def __init__(self, request: Request) -> None:
        self._request = request

    def current_user_id(self) -> UserId:
        user_id = self._request.headers.get(self._USER_ID_HEADER)

        if not user_id:
            raise ApplicationError(
                message="User not provided", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return UserId(UUID(user_id))
