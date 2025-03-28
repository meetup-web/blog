from collections.abc import AsyncIterator

from alembic.config import Config as AlembicConfig
from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import (
    Provider,
    Scope,
    WithParents,
    alias,
    from_context,
    provide,
    provide_all,
)
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from blog.application.common.behaviors.commition_behavior import (
    CommitionBehavior,
)
from blog.application.common.behaviors.event_id_generation_behavior import (
    EventIdGenerationBehavior,
)
from blog.application.common.behaviors.event_publishing_behavior import (
    EventPublishingBehavior,
)
from blog.application.common.markers.command import Command
from blog.application.operations.read.get_comment_by_id import (
    GetCommentById,
    GetCommentByIdHandler,
)
from blog.application.operations.read.get_post_by_id import (
    GetPostById,
    GetPostByIdHandler,
)
from blog.application.operations.read.get_post_comments import (
    GetPostComments,
    GetPostCommentsHandler,
)
from blog.application.operations.write.add_comment import (
    AddComment,
    AddCommentHandler,
)
from blog.application.operations.write.create_post import (
    CreatePost,
    CreatePostHandler,
)
from blog.application.operations.write.delete_comment import (
    DeleteComment,
    DeleteCommentHandler,
)
from blog.application.operations.write.edit_comment import (
    EditComment,
    EditCommentHandler,
)
from blog.application.operations.write.edit_post import (
    EditPost,
    EditPostHandler,
)
from blog.application.ports.committer import Committer
from blog.bootstrap.config import (
    DatabaseConfig,
    RabbitmqConfig,
)
from blog.domain.shared.events import DomainEvent
from blog.infrastructure.domain_events import DomainEvents
from blog.infrastructure.outbox.adapters.rabbitmq_outbox_publisher import (
    RabbitmqOutboxPublisher,
)
from blog.infrastructure.outbox.outbox_processor import OutboxProcessor
from blog.infrastructure.outbox.outbox_publisher import OutboxPublisher
from blog.infrastructure.outbox.outbox_storing_handler import (
    OutboxStoringHandler,
)
from blog.infrastructure.persistence.adapters.sql_comment_gateway import (
    SqlCommentGateway,
)
from blog.infrastructure.persistence.adapters.sql_comment_repository import (
    SqlCommentRepository,
)
from blog.infrastructure.persistence.adapters.sql_outbox_gateway import (
    SqlOutboxGateway,
)
from blog.infrastructure.persistence.adapters.sql_post_gateway import (
    SqlPostGateway,
)
from blog.infrastructure.persistence.adapters.sql_post_repository import (
    SqlPostRepository,
)
from blog.infrastructure.persistence.transaction import Transaction
from blog.infrastructure.post_factory_impl import PostFactoryImpl
from blog.infrastructure.utc_time_provider import UtcTimeProvider
from blog.infrastructure.uuid7_id_generator import UUID7IdGenerator
from blog.presentation.api.htpp_identity_provider import HttpIdentityProvider


class ApiConfigProvider(Provider):
    scope = Scope.APP

    rabbitmq_config = from_context(RabbitmqConfig)
    database_config = from_context(DatabaseConfig)


class PersistenceProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def engine(self, postgres_config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(postgres_config.uri)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

    @provide(provides=AsyncSession)
    async def session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session


class DomainAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(
        WithParents[SqlPostRepository],  # type: ignore[misc]
        WithParents[SqlCommentRepository],  # type: ignore[misc]
    )
    domain_events = provide(WithParents[DomainEvents])  # type: ignore[misc]
    post_factory = provide(WithParents[PostFactoryImpl])  # type: ignore[misc]


class ApplicationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    gateways = provide_all(
        WithParents[SqlPostGateway],  # type: ignore[misc]
        WithParents[SqlOutboxGateway],  # type: ignore[misc]
        WithParents[SqlCommentGateway],  # type: ignore[misc]
    )
    id_generator = provide(
        WithParents[UUID7IdGenerator],  # type: ignore[misc]
        scope=Scope.APP,
    )
    time_provider = provide(
        WithParents[UtcTimeProvider],  # type: ignore[misc]
        scope=Scope.APP,
    )
    committer = alias(AsyncSession, provides=Committer)


class AuthProvider(Provider):
    scope = Scope.REQUEST

    identity_provider = provide(
        WithParents[HttpIdentityProvider],  # type: ignore[misc]
    )


class InfrastructureAdaptersProvider(Provider):
    scope = Scope.REQUEST

    transaction = alias(AsyncSession, provides=Transaction)


class ApplicationHandlersProvider(Provider):
    scope = Scope.REQUEST

    handlers = provide_all(
        EditPostHandler,
        CreatePostHandler,
        AddCommentHandler,
        EditCommentHandler,
        DeleteCommentHandler,
        GetCommentByIdHandler,
        GetPostCommentsHandler,
        GetCommentByIdHandler,
        OutboxStoringHandler,
        GetPostByIdHandler,
    )
    behaviors = provide_all(
        CommitionBehavior,
        EventPublishingBehavior,
        EventIdGenerationBehavior,
    )


class BazarioProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(EditPost, EditPostHandler)
        registry.add_request_handler(CreatePost, CreatePostHandler)
        registry.add_request_handler(AddComment, AddCommentHandler)
        registry.add_request_handler(EditComment, EditCommentHandler)
        registry.add_request_handler(DeleteComment, DeleteCommentHandler)
        registry.add_request_handler(GetPostById, GetPostByIdHandler)
        registry.add_request_handler(GetPostComments, GetPostCommentsHandler)
        registry.add_request_handler(GetCommentById, GetCommentByIdHandler)
        registry.add_notification_handlers(DomainEvent, OutboxStoringHandler)
        registry.add_pipeline_behaviors(DomainEvent, EventIdGenerationBehavior)
        registry.add_pipeline_behaviors(
            Command,
            EventPublishingBehavior,
            CommitionBehavior,
        )

        return registry

    resolver = provide(WithParents[DishkaResolver])  # type: ignore[misc]
    dispatcher = provide(WithParents[Dispatcher])  # type: ignore[misc]


class CliConfigProvider(Provider):
    scope = Scope.APP

    alembic_config = from_context(AlembicConfig)
    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)


class BrokerProvider(Provider):
    scope = Scope.APP

    faststream_rabbit_broker = from_context(RabbitBroker)


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def outbox_publisher(
        self,
        broker: RabbitBroker,
    ) -> OutboxPublisher:
        return RabbitmqOutboxPublisher(broker=broker)

    @provide
    async def outbox_processor(
        self,
        transaction: Transaction,
        outbox_gateway: SqlOutboxGateway,
        outbox_publisher: OutboxPublisher,
    ) -> OutboxProcessor:
        return OutboxProcessor(
            transaction=transaction,
            outbox_gateway=outbox_gateway,
            outbox_publisher=outbox_publisher,
        )
