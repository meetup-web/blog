from blog.application.ports.id_generator import IdGenerator
from blog.application.ports.time_provider import TimeProvider
from blog.domain.posts.events import PostCreated
from blog.domain.posts.factory import PostFactory
from blog.domain.posts.post import Post
from blog.domain.shared.events import DomainEventAdder
from blog.domain.shared.unit_of_work import UnitOfWork
from blog.domain.shared.user_id import UserId


class PostFactoryImpl(PostFactory):
    def __init__(
        self,
        id_generator: IdGenerator,
        unit_of_work: UnitOfWork,
        time_provider: TimeProvider,
        domain_event_adder: DomainEventAdder,
    ) -> None:
        self._id_generator = id_generator
        self._unit_of_work = unit_of_work
        self._time_provider = time_provider
        self._domain_event_adder = domain_event_adder

    def create(self, title: str, content: str, creator_id: UserId) -> Post:
        post_id = self._id_generator.generate_post_id()
        current_time = self._time_provider.provide_current()

        post = Post(
            title=title,
            content=content,
            entity_id=post_id,
            created_at=current_time,
            unit_of_work=self._unit_of_work,
            event_adder=self._domain_event_adder,
            creator_id=creator_id,
        )
        post.add_event(
            PostCreated(
                title=title,
                content=content,
                post_id=post_id,
                event_date=current_time,
                creator_id=creator_id,
            )
        )
        return post
