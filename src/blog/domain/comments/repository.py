from abc import ABC, abstractmethod

from blog.domain.comments.comment import Comment
from blog.domain.comments.comment_id import CommentId
from blog.domain.posts.post_id import PostId
from blog.domain.shared.user_id import UserId


class CommentRepository(ABC):
    @abstractmethod
    def add(self, comment: Comment) -> None: ...
    @abstractmethod
    async def delete(self, comment: Comment) -> None: ...
    @abstractmethod
    async def load(self, comment_id: CommentId) -> Comment | None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[Comment]: ...
    @abstractmethod
    async def with_post_id(self, post_id: PostId) -> list[Comment]: ...
