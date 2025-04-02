from dataclasses import dataclass

from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class UserDeleted:
    user_id: UserId
