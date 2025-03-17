from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from blog.application.models.comment import CommentReadModel
from blog.application.models.pagination import Pagination
from blog.application.ports.comment_gateway import CommentGateway
from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId
from blog.infrastructure.persistence.sql_tables import COMMENTS_TABLE


class SqlCommentGateway(CommentGateway):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection
        self._identity_map: dict[CommentId, CommentReadModel] = {}

    async def with_id(self, comment_id: CommentId) -> CommentReadModel | None:
        if comment_id in self._identity_map:
            return self._identity_map[comment_id]

        statement = select(
            COMMENTS_TABLE.c.post_id.label("post_id"),
            COMMENTS_TABLE.c.content.label("content"),
            COMMENTS_TABLE.c.comment_id.label("comment_id"),
            COMMENTS_TABLE.c.created_at.label("created_at"),
            COMMENTS_TABLE.c.updated_at.label("updated_at"),
            COMMENTS_TABLE.c.creator_id.label("creator_id"),
        ).where(COMMENTS_TABLE.c.comment_id == comment_id)
        cursor_result = await self._connection.execute(statement)
        cursor_row: Row | None = cursor_result.fetchone()

        if not cursor_row:
            return None

        return self._load(cursor_row)

    async def with_post_id(
        self,
        post_id: PostId,
        pagination: Pagination,
    ) -> list[CommentReadModel]:
        statement = (
            select(
                COMMENTS_TABLE.c.post_id.label("post_id"),
                COMMENTS_TABLE.c.content.label("content"),
                COMMENTS_TABLE.c.comment_id.label("comment_id"),
                COMMENTS_TABLE.c.created_at.label("created_at"),
                COMMENTS_TABLE.c.updated_at.label("updated_at"),
                COMMENTS_TABLE.c.creator_id.label("creator_id"),
            )
            .where(COMMENTS_TABLE.c.post_id == post_id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        cursor_result = await self._connection.execute(statement)

        comments: list[CommentReadModel] = []
        for cursor_row in cursor_result:
            comments.append(comment := self._load(cursor_row))
            self._identity_map[comment.comment_id] = comment

        return comments

    def _load(self, cursor_row: Row) -> CommentReadModel:
        return CommentReadModel(
            content=cursor_row.content,
            post_id=cursor_row.post_id,
            comment_id=cursor_row.comment_id,
            created_at=cursor_row.created_at,
            updated_at=cursor_row.updated_at,
            creator_id=cursor_row.creator_id,
        )
