from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.markers.command import Command
from blog.application.ports.time_provider import TimeProvider
from blog.domain.posts.events import PostDeleted
from blog.domain.posts.repository import PostRepository
from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class DeleteUserPosts(Command[None]):
    user_id: UserId


class DeleteUserPostsHandler(RequestHandler[DeleteUserPosts, None]):
    def __init__(
        self,
        post_repository: PostRepository,
        time_provider: TimeProvider,
    ) -> None:
        self._post_repository = post_repository
        self._time_provider = time_provider

    async def handle(self, request: DeleteUserPosts) -> None:
        posts = await self._post_repository.with_user_id(request.user_id)

        for post in posts:
            event = PostDeleted(
                post_id=post.entity_id,
                event_date=self._time_provider.provide_current(),
            )

            post.add_event(event)
            await self._post_repository.delete(post)
