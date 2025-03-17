from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from blog.application.common.markers.query import Query
from blog.application.models.comment import CommentReadModel
from blog.application.ports.comment_gateway import CommentGateway
from blog.domain.comments.comment_id import CommentId


@dataclass(frozen=True)
class GetCommentById(Query[CommentReadModel]):
    comment_id: CommentId


class GetCommentByIdHandler(RequestHandler[GetCommentById, CommentReadModel]):
    def __init__(self, comment_gateway: CommentGateway) -> None:
        self._comment_gateway = comment_gateway

    async def handle(self, request: GetCommentById) -> CommentReadModel:
        comment = await self._comment_gateway.with_id(request.comment_id)

        if comment is None:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Comment with id {request.comment_id} not found",
            )

        return comment
