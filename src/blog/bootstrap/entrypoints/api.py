from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, cast

from dishka.integrations.fastapi import (
    setup_dishka as add_container_to_fastapi,
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from blog.application.common.application_error import ApplicationError
from blog.bootstrap.config import get_database_config, get_rabbitmq_config
from blog.bootstrap.container import bootstrap_api_container
from blog.bootstrap.entrypoints.stream import bootstrap_stream
from blog.infrastructure.persistence.sql_tables import (
    map_comments_table,
    map_outbox_table,
    map_posts_table,
)
from blog.presentation.api.exception_handlers import application_error_handler
from blog.presentation.api.routers.comments import COMMENTS_ROUTER
from blog.presentation.api.routers.healthcheck import HEALTHCHECK_ROUTER
from blog.presentation.api.routers.posts import POSTS_ROUTER

if TYPE_CHECKING:
    from starlette.types import HTTPExceptionHandler


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    map_comments_table()
    map_outbox_table()
    map_posts_table()
    stream = bootstrap_stream()
    await stream.start()
    yield
    await stream.stop()


def add_middlewares(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


def add_api_routers(application: FastAPI) -> None:
    application.include_router(POSTS_ROUTER)
    application.include_router(COMMENTS_ROUTER)
    application.include_router(HEALTHCHECK_ROUTER)


def add_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(
        ApplicationError,
        cast("HTTPExceptionHandler", application_error_handler),
    )


def bootstrap_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    dishka_container = bootstrap_api_container(
        get_rabbitmq_config(),
        get_database_config(),
    )

    add_middlewares(application)
    add_api_routers(application)
    add_exception_handlers(application)
    add_container_to_fastapi(dishka_container, application)

    return application
