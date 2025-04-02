from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.markers.command import Command
from blog.application.ports.time_provider import TimeProvider
from blog.domain.comments.events import CommentDeleted
from blog.domain.comments.repository import CommentRepository
from blog.domain.shared.user_id import UserId


@dataclass(frozen=True)
class DeleteUserComments(Command[None]):
    user_id: UserId


class DeleteUserCommentsHandler(RequestHandler[DeleteUserComments, None]):
    def __init__(
        self, comment_repository: CommentRepository, time_provider: TimeProvider
    ) -> None:
        self._comment_repository = comment_repository
        self._time_provider = time_provider

    async def handle(self, request: DeleteUserComments) -> None:
        comments = await self._comment_repository.with_user_id(request.user_id)

        for comment in comments:
            event = CommentDeleted(
                comment_id=comment.entity_id,
                post_id=comment.post_id,
                event_date=self._time_provider.provide_current(),
            )

            comment.add_event(event)
            await self._comment_repository.delete(comment)
