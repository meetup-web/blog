from abc import ABC, abstractmethod

from blog.application.models.comment import CommentReadModel
from blog.application.models.pagination import Pagination
from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId


class CommentGateway(ABC):
    @abstractmethod
    async def with_id(self, comment_id: CommentId) -> CommentReadModel | None: ...
    @abstractmethod
    async def with_post_id(
        self,
        post_id: PostId,
        pagination: Pagination,
    ) -> list[CommentReadModel]: ...
