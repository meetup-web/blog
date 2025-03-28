from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from blog.application.common.markers.command import Command
from blog.application.ports.context.identity_provider import IdentityProvider
from blog.application.ports.time_provider import TimeProvider
from blog.domain.comments.comment_id import CommentId
from blog.domain.comments.repository import CommentRepository


@dataclass(frozen=True)
class EditComment(Command[None]):
    new_content: str
    comment_id: CommentId


class EditCommentHandler(RequestHandler[EditComment, None]):
    def __init__(
        self,
        time_provider: TimeProvider,
        comment_repository: CommentRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._time_provider = time_provider
        self._comment_repository = comment_repository
        self._identity_provider = identity_provider

    async def handle(self, request: EditComment) -> None:
        current_user_id = await self._identity_provider.current_user_id()
        comment = await self._comment_repository.load(request.comment_id)

        if comment is None:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Comment with id {request.comment_id} not found",
            )

        if comment.creator_id != current_user_id:
            raise ApplicationError(
                error_type=ErrorType.PERMISSION_ERROR,
                message="You are not allowed to edit this comment",
            )

        comment.edit(request.new_content, self._time_provider.provide_current())
