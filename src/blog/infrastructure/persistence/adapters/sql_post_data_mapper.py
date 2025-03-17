from sqlalchemy.ext.asyncio import AsyncConnection

from blog.domain.posts.post import Post
from blog.infrastructure.persistence.data_mapper import DataMapper
from blog.infrastructure.persistence.sql_tables import POSTS_TABLE


class SqlPostDataMapper(DataMapper[Post]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: Post) -> None:
        statement = POSTS_TABLE.insert().values(
            title=entity.title,
            content=entity.content,
            post_id=entity.entity_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            creator_id=entity.creator_id,
        )
        await self._connection.execute(statement)

    async def update(self, entity: Post) -> None:
        statement = (
            POSTS_TABLE.update()
            .values(
                title=entity.title,
                content=entity.content,
                post_id=entity.entity_id,
                updated_at=entity.updated_at,
            )
            .where(POSTS_TABLE.c.post_id == entity.entity_id)
        )
        await self._connection.execute(statement)

    async def delete(self, entity: Post) -> None:
        statement = POSTS_TABLE.delete().where(POSTS_TABLE.c.post_id == entity.entity_id)
        await self._connection.execute(statement)
