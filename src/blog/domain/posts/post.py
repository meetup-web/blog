from datetime import datetime

from blog.domain.comments.comment import Comment
from blog.domain.comments.comment_id import CommentId
from blog.domain.comments.events import CommentAdded
from blog.domain.posts.events import PostContentChanged, PostTitleChanged
from blog.domain.posts.post_id import PostId
from blog.domain.shared.entity import (
    Entity,
)
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.user_id import UserId


class Post(Entity[PostId]):
    def __init__(
        self,
        entity_id: PostId,
        event_adder: DomainEventAdder,
        *,
        creator_id: UserId,
        title: str,
        content: str,
        created_at: datetime,
        updated_at: datetime | None = None,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder)

        self._title = title
        self._content = content
        self._created_at = created_at
        self._updated_at = updated_at
        self._creator_id = creator_id

    def create_comment(
        self,
        comment_id: CommentId,
        content: str,
        current_time: datetime,
        creator_id: UserId,
    ) -> Comment:
        comment = Comment(
            comment_id,
            self._event_adder,
            content=content,
            post_id=self._entity_id,
            created_at=current_time,
            creator_id=creator_id,
        )
        comment.add_event(
            CommentAdded(
                comment_id=comment_id,
                post_id=self.entity_id,
                content=content,
                event_date=current_time,
                creator_id=creator_id,
            )
        )
        return comment

    def edit(self, new_title: str, new_content: str, current_time: datetime) -> None:
        self.change_title(new_title, current_time)
        self.change_content(new_content, current_time)

    def change_title(self, new_title: str, current_time: datetime) -> None:
        self._title = new_title
        self._updated_at = current_time

        self.add_event(
            PostTitleChanged(self.entity_id, self.title, event_date=current_time)
        )

    def change_content(self, new_content: str, current_time: datetime) -> None:
        self._content = new_content
        self._updated_at = current_time

        self.add_event(
            PostContentChanged(self.entity_id, self.content, event_date=current_time)
        )

    @property
    def title(self) -> str:
        return self._title

    @property
    def content(self) -> str:
        return self._content

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def creator_id(self) -> UserId:
        return self._creator_id
