from abc import ABC, abstractmethod

from blog.domain.posts.post import Post
from blog.domain.posts.post_id import PostId
from blog.domain.shared.user_id import UserId


class PostRepository(ABC):
    @abstractmethod
    def add(self, post: Post) -> None: ...
    @abstractmethod
    async def delete(self, post: Post) -> None: ...
    @abstractmethod
    async def load(self, post_id: PostId) -> Post | None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[Post]: ...
