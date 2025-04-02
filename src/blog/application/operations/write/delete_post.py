from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from blog.application.common.markers.command import Command
from blog.application.ports.identity_provider import IdentityProvider
from blog.application.ports.time_provider import TimeProvider
from blog.domain.posts.events import PostDeleted
from blog.domain.posts.post_id import PostId
from blog.domain.posts.repository import PostRepository


@dataclass(frozen=True)
class DeletePost(Command[None]):
    post_id: PostId


class DeletePostHandler(RequestHandler[DeletePost, None]):
    def __init__(
        self,
        post_repository: PostRepository,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
    ) -> None:
        self._post_repository = post_repository
        self._identity_provider = identity_provider
        self._time_provider = time_provider

    async def handle(self, request: DeletePost) -> None:
        current_user_id = self._identity_provider.current_user_id()
        post = await self._post_repository.load(request.post_id)

        if post is None:
            raise ApplicationError("Post not found", error_type=ErrorType.NOT_FOUND)

        if post.creator_id != current_user_id:
            raise ApplicationError(
                "You are not allowed to delete this post",
                error_type=ErrorType.PERMISSION_ERROR,
            )

        event = PostDeleted(
            post_id=post.entity_id, event_date=self._time_provider.provide_current()
        )

        post.add_event(event)
        await self._post_repository.delete(post)
