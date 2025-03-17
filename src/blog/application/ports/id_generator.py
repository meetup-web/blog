from abc import ABC, abstractmethod

from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId
from blog.domain.shared.event_id import EventId


class IdGenerator(ABC):
    @abstractmethod
    def generate_post_id(self) -> PostId: ...
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
    @abstractmethod
    def generate_comment_id(self) -> CommentId: ...
