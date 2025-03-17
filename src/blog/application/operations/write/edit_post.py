from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from blog.application.common.markers.command import Command
from blog.application.ports.context.identity_provider import IdentityProvider
from blog.application.ports.time_provider import TimeProvider
from blog.domain.posts.post_id import PostId
from blog.domain.posts.repository import PostRepository


@dataclass(frozen=True)
class EditPost(Command[None]):
    post_id: PostId
    new_title: str
    new_content: str


class EditPostHandler(RequestHandler[EditPost, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        post_repository: PostRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._time_provider = time_provider
        self._post_repository = post_repository
        self._identity_provider = identity_provider

    async def handle(self, request: EditPost) -> None:
        current_user_id = await self._identity_provider.current_user_id()
        post = await self._post_repository.load(request.post_id)

        if not post:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Post with id {request.post_id} not found",
            )

        if current_user_id != post.creator_id:
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="You are not allowed to edit this post",
            )

        post.edit(
            request.new_title,
            request.new_content,
            self._time_provider.provide_current(),
        )
