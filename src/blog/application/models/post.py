from dataclasses import dataclass
from datetime import datetime

from blog.domain.posts.post_id import PostId
from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class PostReadModel:
    post_id: PostId
    creator_id: UserId
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
