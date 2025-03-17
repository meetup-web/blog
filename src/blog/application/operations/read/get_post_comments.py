from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.markers.query import Query
from blog.application.models.comment import CommentReadModel
from blog.application.models.pagination import Pagination
from blog.application.ports.comment_gateway import CommentGateway
from blog.domain.posts.post_id import PostId


@dataclass(frozen=True)
class GetPostComments(Query[list[CommentReadModel]]):
    post_id: PostId
    pagination: Pagination


class GetPostCommentsHandler(RequestHandler[GetPostComments, list[CommentReadModel]]):
    def __init__(self, comment_gateway: CommentGateway) -> None:
        self._comment_gateway = comment_gateway

    async def handle(self, request: GetPostComments) -> list[CommentReadModel]:
        return await self._comment_gateway.with_post_id(
            request.post_id,
            request.pagination,
        )
