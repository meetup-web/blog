from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from blog.domain.posts.post import Post
from blog.domain.posts.post_id import PostId
from blog.domain.posts.repository import PostRepository
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.user_id import UserId
from blog.infrastructure.persistence.sql_tables import POSTS_TABLE


class SqlPostRepository(PostRepository):
    def __init__(
        self,
        session: AsyncSession,
        event_adder: DomainEventAdder,
    ) -> None:
        self._session = session
        self._event_adder = event_adder

    def add(self, post: Post) -> None:
        self._session.add(post)

    async def delete(self, post: Post) -> None:
        await self._session.delete(post)

    async def load(self, post_id: PostId) -> Post | None:
        post = await self._session.get(Post, post_id)

        if post is None:
            return None

        return self._load(post)

    async def with_user_id(self, user_id: UserId) -> list[Post]:
        stmt = select(Post).where(POSTS_TABLE.c.creator_id == user_id)
        posts = (await self._session.execute(stmt)).scalars().all()

        return [self._load(post) for post in posts]

    def _load(self, post: Post) -> Post:
        post.__setattr__("_event_adder", self._event_adder)
        return post
