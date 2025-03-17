from datetime import datetime

from blog.domain.comments.comment_id import CommentId
from blog.domain.comments.events import CommentContentChanged
from blog.domain.posts.post_id import PostId
from blog.domain.shared.entity import (
    Entity,
)
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.unit_of_work import UnitOfWork
from blog.domain.shared.user_id import UserId


class Comment(Entity[CommentId]):
    def __init__(
        self,
        entity_id: CommentId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        creator_id: UserId,
        content: str,
        post_id: PostId,
        created_at: datetime,
        updated_at: datetime | None = None,
    ) -> None:
        super().__init__(entity_id, event_adder, unit_of_work)

        self._content = content
        self._post_id = post_id
        self._created_at = created_at
        self._updated_at = updated_at
        self._creator_id = creator_id

    def edit(self, new_content: str, current_time: datetime) -> None:
        self._content = new_content
        self._updated_at = current_time

        self.add_event(
            CommentContentChanged(
                self.entity_id,
                self.post_id,
                self.content,
                event_date=current_time,
            )
        )
        self.mark_dirty()

    @property
    def post_id(self) -> PostId:
        return self._post_id

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
