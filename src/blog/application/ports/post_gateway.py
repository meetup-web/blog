from abc import ABC, abstractmethod

from blog.application.models.post import PostReadModel
from blog.domain.posts.post_id import PostId


class PostGateway(ABC):
    @abstractmethod
    async def with_id(self, post_id: PostId) -> PostReadModel | None: ...
