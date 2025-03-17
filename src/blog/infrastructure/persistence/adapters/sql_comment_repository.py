from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from blog.domain.comments.comment import Comment
from blog.domain.comments.comment_id import CommentId
from blog.domain.comments.repository import CommentRepository
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.unit_of_work import UnitOfWork
from blog.infrastructure.persistence.sql_tables import COMMENTS_TABLE


class SqlCommentRepository(CommentRepository):
    def __init__(
        self,
        connection: AsyncConnection,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
    ) -> None:
        self._connection = connection
        self._event_adder = event_adder
        self._unit_of_work = unit_of_work
        self._identity_map: dict[CommentId, Comment] = {}

    def add(self, comment: Comment) -> None:
        self._unit_of_work.register_new(comment)
        self._identity_map[comment.entity_id] = comment

    def delete(self, comment: Comment) -> None:
        self._unit_of_work.register_deleted(comment)
        self._identity_map.pop(comment.entity_id, None)

    async def load(self, comment_id: CommentId) -> Comment | None:
        if comment_id in self._identity_map:
            return self._identity_map[comment_id]

        statement = select(
            COMMENTS_TABLE.c.post_id.label("post_id"),
            COMMENTS_TABLE.c.content.label("content"),
            COMMENTS_TABLE.c.comment_id.label("entity_id"),
            COMMENTS_TABLE.c.created_at.label("created_at"),
            COMMENTS_TABLE.c.updated_at.label("updated_at"),
            COMMENTS_TABLE.c.creator_id.label("creator_id"),
        ).where(COMMENTS_TABLE.c.comment_id == comment_id)
        cursor_result = await self._connection.execute(statement)
        cursor_row = cursor_result.fetchone()

        if cursor_row is None:
            return None

        return self._load(cursor_row)

    def _load(self, cursor_row: Row) -> Comment:
        return Comment(
            entity_id=cursor_row.entity_id,
            content=cursor_row.content,
            post_id=cursor_row.post_id,
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            created_at=cursor_row.created_at,
            updated_at=cursor_row.updated_at,
            creator_id=cursor_row.creator_id,
        )
