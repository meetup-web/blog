from abc import ABC, abstractmethod

from blog.domain.comments.comment import Comment
from blog.domain.comments.comment_id import CommentId


class CommentRepository(ABC):
    @abstractmethod
    def add(self, comment: Comment) -> None: ...
    @abstractmethod
    async def delete(self, comment: Comment) -> None: ...
    @abstractmethod
    async def load(self, comment_id: CommentId) -> Comment | None: ...
