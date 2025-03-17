from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from blog.domain.posts.post import Post
from blog.domain.posts.post_id import PostId
from blog.domain.posts.repository import PostRepository
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.unit_of_work import UnitOfWork
from blog.infrastructure.persistence.sql_tables import POSTS_TABLE


class SqlPostRepository(PostRepository):
    def __init__(
        self,
        connection: AsyncConnection,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._connection = connection
        self._event_adder = event_adder
        self._unit_of_work = unit_of_work
        self._identity_map: dict[PostId, Post] = {}

    def add(self, post: Post) -> None:
        self._unit_of_work.register_new(post)
        self._identity_map[post.entity_id] = post

    def delete(self, post: Post) -> None:
        self._unit_of_work.register_deleted(post)
        self._identity_map.pop(post.entity_id, None)

    async def load(self, post_id: PostId) -> Post | None:
        if post_id in self._identity_map:
            return self._identity_map[post_id]

        statement = select(
            POSTS_TABLE.c.title.label("title"),
            POSTS_TABLE.c.content.label("content"),
            POSTS_TABLE.c.post_id.label("entity_id"),
            POSTS_TABLE.c.created_at.label("created_at"),
            POSTS_TABLE.c.updated_at.label("updated_at"),
            POSTS_TABLE.c.creator_id.label("creator_id"),
        ).where(POSTS_TABLE.c.post_id == post_id)
        cursor_result = await self._connection.execute(statement)
        cursor_row = cursor_result.fetchone()

        if cursor_row is None:
            return None

        return self._load(cursor_row)

    def _load(self, cursor_row: Row) -> Post:
        return Post(
            title=cursor_row.title,
            content=cursor_row.content,
            event_adder=self._event_adder,
            entity_id=cursor_row.entity_id,
            unit_of_work=self._unit_of_work,
            created_at=cursor_row.created_at,
            updated_at=cursor_row.updated_at,
            creator_id=cursor_row.creator_id,
        )
