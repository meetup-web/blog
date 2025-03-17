from dataclasses import dataclass

from blog.domain.posts.post_id import PostId
from blog.domain.shared.events import DomainEvent
from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class PostCreated(DomainEvent):
    post_id: PostId
    creator_id: UserId
    title: str
    content: str


@dataclass(frozen=True)
class PostDeleted(DomainEvent):
    post_id: PostId


@dataclass(frozen=True)
class PostTitleChanged(DomainEvent):
    post_id: PostId
    title: str


@dataclass(frozen=True)
class PostContentChanged(DomainEvent):
    post_id: PostId
    content: str
