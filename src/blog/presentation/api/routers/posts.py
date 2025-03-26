from typing import Annotated

from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from blog.application.common.application_error import ApplicationError
from blog.application.models.comment import CommentReadModel
from blog.application.models.pagination import Pagination
from blog.application.models.post import PostReadModel
from blog.application.operations.read.get_post_by_id import GetPostById
from blog.application.operations.read.get_post_comments import GetPostComments
from blog.application.operations.write.create_post import CreatePost
from blog.application.operations.write.edit_post import EditPost
from blog.domain.posts.post_id import PostId
from blog.presentation.api.response_models import ErrorResponse, SuccessResponse

POSTS_ROUTER = APIRouter(prefix="/posts", tags=["posts"])


@POSTS_ROUTER.post(
    path="/",
    responses={
        HTTP_201_CREATED: {"model": SuccessResponse[PostId]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_201_CREATED,
)
@inject
async def create_post(
    request: CreatePost,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[PostId]:
    post_id = await sender.send(request)
    return SuccessResponse(result=post_id, status=HTTP_201_CREATED)


@POSTS_ROUTER.put(
    path="/{post_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
        HTTP_403_FORBIDDEN: {"model": ErrorResponse[ApplicationError]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def edit_post(
    post_id: PostId,
    new_title: Annotated[str, Body()],
    new_content: Annotated[str, Body()],
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(EditPost(post_id, new_title, new_content))
    return SuccessResponse(status=HTTP_200_OK)


@POSTS_ROUTER.get(
    path="/{post_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[PostReadModel]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def get_post_by_id(
    post_id: PostId,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[PostReadModel]:
    post = await sender.send(GetPostById(post_id))
    return SuccessResponse(status=HTTP_200_OK, result=post)


@POSTS_ROUTER.get(
    path="/{post_id}/comments",
    responses={HTTP_200_OK: {"model": SuccessResponse[list[CommentReadModel]]}},
    status_code=HTTP_200_OK,
)
@inject
async def get_post_comments(
    post_id: PostId,
    pagination: Annotated[
        Pagination,
        Depends(),
    ],
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[list[CommentReadModel]]:
    comments = await sender.send(GetPostComments(post_id, pagination))
    return SuccessResponse(status=HTTP_200_OK, result=comments)
