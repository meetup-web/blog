from abc import ABC, abstractmethod

from blog.domain.posts.post import Post
from blog.domain.posts.post_id import PostId


class PostRepository(ABC):
    @abstractmethod
    def add(self, post: Post) -> None: ...
    @abstractmethod
    def delete(self, post: Post) -> None: ...
    @abstractmethod
    async def load(self, post_id: PostId) -> Post | None: ...
