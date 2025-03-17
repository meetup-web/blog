from sqlalchemy import UUID, Column, DateTime, ForeignKey, MetaData, Table, Text

METADATA = MetaData()

POSTS_TABLE = Table(
    "posts",
    METADATA,
    Column("post_id", UUID, primary_key=True),
    Column("title", Text, nullable=False),
    Column("content", Text, nullable=False),
    Column("creator_id", UUID, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


COMMENTS_TABLE = Table(
    "comments",
    METADATA,
    Column("comment_id", UUID, primary_key=True),
    Column("post_id", ForeignKey("posts.post_id"), nullable=False),
    Column("content", Text, nullable=False),
    Column("creator_id", UUID, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)


OUTBOX_TABLE = Table(
    "outbox",
    METADATA,
    Column("message_id", UUID, primary_key=True),
    Column("data", Text, nullable=False),
    Column("event_type", Text, nullable=False, default=False),
)
