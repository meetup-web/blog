from uuid import UUID

from blog.application.ports.context.identity_provider import IdentityProvider
from blog.application.ports.context.user_role import UserRole
from blog.domain.shared.user_id import UserId


class FakeIdentityProvider(IdentityProvider):
    async def current_user_id(self) -> UserId:
        return UserId(UUID("067c3205-d896-7404-8000-3c25a05b74cf"))

    async def current_user_role(self) -> UserRole:
        return UserRole.ADMIN
