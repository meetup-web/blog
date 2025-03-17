from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from blog.application.common.markers.query import Query
from blog.application.models.post import PostReadModel
from blog.application.ports.post_gateway import PostGateway
from blog.domain.posts.post_id import PostId


@dataclass(frozen=True)
class GetPostById(Query[PostReadModel]):
    post_id: PostId


class GetPostByIdHandler(RequestHandler[GetPostById, PostReadModel]):
    def __init__(self, post_gateway: PostGateway) -> None:
        self._post_gateway = post_gateway

    async def handle(self, request: GetPostById) -> PostReadModel:
        post = await self._post_gateway.with_id(request.post_id)

        if post is None:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND,
                message=f"Post with id {request.post_id} not found",
            )

        return post
