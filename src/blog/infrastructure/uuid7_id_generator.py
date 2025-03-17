from uuid_extensions import uuid7  # type: ignore

from blog.application.ports.id_generator import IdGenerator
from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId
from blog.domain.shared.event_id import EventId


class UUID7IdGenerator(IdGenerator):
    def generate_post_id(self) -> PostId:
        return PostId(uuid7())

    def generate_event_id(self) -> EventId:
        return EventId(uuid7())

    def generate_comment_id(self) -> CommentId:
        return CommentId(uuid7())
