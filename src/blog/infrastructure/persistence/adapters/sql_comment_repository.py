from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from blog.domain.comments.comment import Comment
from blog.domain.comments.comment_id import CommentId
from blog.domain.comments.repository import CommentRepository
from blog.domain.posts.post_id import PostId
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.user_id import UserId
from blog.infrastructure.persistence.sql_tables import COMMENTS_TABLE


class SqlCommentRepository(CommentRepository):
    def __init__(
        self,
        session: AsyncSession,
        event_adder: DomainEventAdder,
    ) -> None:
        self._session = session
        self._event_adder = event_adder

    def add(self, comment: Comment) -> None:
        self._session.add(comment)

    async def delete(self, comment: Comment) -> None:
        await self._session.delete(comment)

    async def load(self, comment_id: CommentId) -> Comment | None:
        comment = await self._session.get(Comment, comment_id)

        if comment is None:
            return None

        return self._load(comment)

    async def with_user_id(self, user_id: UserId) -> list[Comment]:
        stmt = select(Comment).where(COMMENTS_TABLE.c.creator_id == user_id)
        comments = (await self._session.execute(stmt)).scalars().all()

        return [self._load(comment) for comment in comments]

    async def with_post_id(self, post_id: PostId) -> list[Comment]:
        stmt = select(Comment).where(COMMENTS_TABLE.c.post_id == post_id)
        comments = (await self._session.execute(stmt)).scalars().all()

        return [self._load(comment) for comment in comments]

    def _load(self, comment: Comment) -> Comment:
        comment.__setattr__("_event_adder", self._event_adder)
        return comment
