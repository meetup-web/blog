from dataclasses import dataclass
from datetime import datetime

from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId
from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class CommentReadModel:
    comment_id: CommentId
    post_id: PostId
    creator_id: UserId
    content: str
    created_at: datetime
    updated_at: datetime
