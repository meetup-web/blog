from bazario.asyncio import NotificationHandler

from blog.domain.comments.repository import CommentRepository
from blog.domain.posts.events import PostDeleted


class RemoveCommentsOnPostDeletedHandler(NotificationHandler[PostDeleted]):
    def __init__(self, comment_repository: CommentRepository) -> None:
        self._comment_repository = comment_repository

    async def handle(self, notification: PostDeleted) -> None:
        comments = await self._comment_repository.with_post_id(notification.post_id)

        for comment in comments:
            await self._comment_repository.delete(comment)
