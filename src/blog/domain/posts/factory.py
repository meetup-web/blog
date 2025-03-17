from abc import ABC, abstractmethod

from blog.domain.posts.post import Post
from blog.domain.shared.user_id import UserId


class PostFactory(ABC):
    @abstractmethod
    def create(self, title: str, content: str, creator_id: UserId) -> Post: ...
