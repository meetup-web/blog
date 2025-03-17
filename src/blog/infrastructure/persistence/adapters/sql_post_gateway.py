from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from blog.application.models.post import PostReadModel
from blog.application.ports.post_gateway import PostGateway
from blog.domain.posts.post_id import PostId
from blog.infrastructure.persistence.sql_tables import POSTS_TABLE


class SqlPostGateway(PostGateway):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection
        self._identity_map: dict[PostId, PostReadModel] = {}

    async def with_id(self, post_id: PostId) -> PostReadModel | None:
        if post_id in self._identity_map:
            return self._identity_map[post_id]

        statement = select(
            POSTS_TABLE.c.title.label("title"),
            POSTS_TABLE.c.content.label("content"),
            POSTS_TABLE.c.post_id.label("post_id"),
            POSTS_TABLE.c.created_at.label("created_at"),
            POSTS_TABLE.c.updated_at.label("updated_at"),
            POSTS_TABLE.c.creator_id.label("creator_id"),
        ).where(POSTS_TABLE.c.post_id == post_id)
        cursor_result = await self._connection.execute(statement)
        cursor_row = cursor_result.fetchone()

        if cursor_row is None:
            return None

        return self._load(cursor_row)

    def _load(self, cursor_row: Row) -> PostReadModel:
        return PostReadModel(
            title=cursor_row.title,
            content=cursor_row.content,
            post_id=cursor_row.post_id,
            created_at=cursor_row.created_at,
            updated_at=cursor_row.updated_at,
            creator_id=cursor_row.creator_id,
        )
