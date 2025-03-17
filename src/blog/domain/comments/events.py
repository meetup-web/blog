from dataclasses import dataclass

from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId
from blog.domain.shared.events import DomainEvent
from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class CommentAdded(DomainEvent):
    comment_id: CommentId
    post_id: PostId
    creator_id: UserId
    content: str


@dataclass(frozen=True)
class CommentContentChanged(DomainEvent):
    comment_id: CommentId
    post_id: PostId
    content: str


@dataclass(frozen=True)
class CommentDeleted(DomainEvent):
    comment_id: CommentId
    post_id: PostId
