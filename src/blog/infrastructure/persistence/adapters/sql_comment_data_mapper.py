from sqlalchemy.ext.asyncio import AsyncConnection

from blog.domain.comments.comment import Comment
from blog.infrastructure.persistence.data_mapper import DataMapper
from blog.infrastructure.persistence.sql_tables import COMMENTS_TABLE


class SqlCommentDataMapper(DataMapper[Comment]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: Comment) -> None:
        statement = COMMENTS_TABLE.insert().values(
            post_id=entity.post_id,
            creator_id=entity.creator_id,
            content=entity.content,
            comment_id=entity.entity_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        await self._connection.execute(statement)

    async def update(self, entity: Comment) -> None:
        statement = (
            COMMENTS_TABLE.update()
            .values(
                content=entity.content,
                comment_id=entity.entity_id,
                updated_at=entity.updated_at,
            )
            .where(COMMENTS_TABLE.c.comment_id == entity.entity_id)
        )
        await self._connection.execute(statement)

    async def delete(self, entity: Comment) -> None:
        statement = COMMENTS_TABLE.delete().where(
            COMMENTS_TABLE.c.comment_id == entity.entity_id
        )
        await self._connection.execute(statement)
