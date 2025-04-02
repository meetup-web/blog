from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from blog.application.common.markers.command import Command
from blog.application.ports.id_generator import IdGenerator
from blog.application.ports.identity_provider import IdentityProvider
from blog.application.ports.time_provider import TimeProvider
from blog.domain.comments.comment_id import CommentId
from blog.domain.comments.repository import CommentRepository
from blog.domain.posts.post_id import PostId
from blog.domain.posts.repository import PostRepository


@dataclass(frozen=True)
class AddComment(Command[CommentId]):
    content: str
    post_id: PostId


class AddCommentHandler(RequestHandler[AddComment, CommentId]):
    def __init__(
        self,
        id_generator: IdGenerator,
        time_provider: TimeProvider,
        post_repository: PostRepository,
        comment_repository: CommentRepository,
        identitiy_provider: IdentityProvider,
    ) -> None:
        self._id_generator = id_generator
        self._time_provider = time_provider
        self._post_repository = post_repository
        self._comment_repository = comment_repository
        self._identity_provider = identitiy_provider

    async def handle(self, request: AddComment) -> CommentId:
        current_user_id = self._identity_provider.current_user_id()
        post = await self._post_repository.load(request.post_id)

        if post is None:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Post with id {request.post_id} not found",
            )

        comment = post.create_comment(
            creator_id=current_user_id,
            content=request.content,
            current_time=self._time_provider.provide_current(),
            comment_id=self._id_generator.generate_comment_id(),
        )
        self._comment_repository.add(comment)

        return comment.entity_id
