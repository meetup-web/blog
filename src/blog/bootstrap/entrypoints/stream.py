from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.faststream import (
    setup_dishka as add_container_to_faststream,
)
from faststream import ContextRepo, FastStream
from faststream.rabbit.broker import RabbitBroker

from blog.bootstrap.config import get_database_config, get_rabbitmq_config
from blog.bootstrap.container import (
    bootstrap_api_container as bootstrap_stream_container,
)
from blog.infrastructure.persistence.sql_tables import (
    map_comments_table,
    map_outbox_table,
    map_posts_table,
)
from blog.presentation.stream.exception_handlers import fastream_exception_middleware
from blog.presentation.stream.routers.comments import COMMENTS_ROUTER
from blog.presentation.stream.routers.posts import POSTS_ROUTER


@asynccontextmanager
async def lifespan(context: ContextRepo) -> AsyncGenerator[None, None]:
    map_comments_table()
    map_outbox_table()
    map_posts_table()

    yield


def add_middlewares(broker: RabbitBroker) -> None:
    broker.add_middleware(middleware=fastream_exception_middleware())


def add_consumers(broker: RabbitBroker) -> None:
    broker.include_router(POSTS_ROUTER)
    broker.include_router(COMMENTS_ROUTER)


def bootstrap_stream() -> FastStream:
    rabbit_config = get_rabbitmq_config()
    broker = RabbitBroker(rabbit_config.uri)

    add_middlewares(broker=broker)
    add_consumers(broker=broker)

    application = FastStream(broker=broker, lifespan=lifespan)
    container = bootstrap_stream_container(
        rabbitmq_config=rabbit_config,
        database_config=get_database_config(),
    )
    add_container_to_faststream(container=container, app=application)

    return application
