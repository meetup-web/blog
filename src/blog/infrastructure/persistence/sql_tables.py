from sqlalchemy import UUID, Column, DateTime, ForeignKey, MetaData, Table, Text
from sqlalchemy.orm import registry

from blog.domain.comments.comment import Comment
from blog.domain.posts.post import Post
from blog.infrastructure.outbox.outbox_message import OutboxMessage

METADATA = MetaData()
MAPPER_REGISTRY = registry(metadata=METADATA)

POSTS_TABLE = Table(
    "posts",
    MAPPER_REGISTRY.metadata,
    Column("post_id", UUID, primary_key=True),
    Column("title", Text, nullable=False),
    Column("content", Text, nullable=False),
    Column("creator_id", UUID, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


COMMENTS_TABLE = Table(
    "comments",
    MAPPER_REGISTRY.metadata,
    Column("comment_id", UUID, primary_key=True),
    Column("post_id", ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False),
    Column("content", Text, nullable=False),
    Column("creator_id", UUID, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


OUTBOX_TABLE = Table(
    "outbox",
    MAPPER_REGISTRY.metadata,
    Column("message_id", UUID, primary_key=True),
    Column("data", Text, nullable=False),
    Column("event_type", Text, nullable=False, default=False),
)


def map_posts_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Post,
        POSTS_TABLE,
        properties={
            "_entity_id": POSTS_TABLE.c.post_id,
            "_title": POSTS_TABLE.c.title,
            "_content": POSTS_TABLE.c.content,
            "_created_at": POSTS_TABLE.c.created_at,
            "_creator_id": POSTS_TABLE.c.creator_id,
            "_updated_at": POSTS_TABLE.c.updated_at,
        },
    )


def map_comments_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Comment,
        COMMENTS_TABLE,
        properties={
            "_entity_id": COMMENTS_TABLE.c.comment_id,
            "_post_id": COMMENTS_TABLE.c.post_id,
            "_content": COMMENTS_TABLE.c.content,
            "_created_at": COMMENTS_TABLE.c.created_at,
            "_creator_id": COMMENTS_TABLE.c.creator_id,
            "_updated_at": COMMENTS_TABLE.c.updated_at,
        },
    )


def map_outbox_table() -> None:
    MAPPER_REGISTRY.map_imperatively(OutboxMessage, OUTBOX_TABLE)
