from abc import ABC, abstractmethod

from blog.application.ports.context.user_role import UserRole
from blog.domain.shared.user_id import UserId


class IdentityProvider(ABC):
    @abstractmethod
    async def current_user_id(self) -> UserId: ...
    @abstractmethod
    async def current_user_role(self) -> UserRole: ...
