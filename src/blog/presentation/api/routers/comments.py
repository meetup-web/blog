from typing import Annotated

from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Body
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from blog.application.common.application_error import ApplicationError
from blog.application.models.comment import CommentReadModel
from blog.application.operations.read.get_comment_by_id import GetCommentById
from blog.application.operations.write.add_comment import AddComment
from blog.application.operations.write.delete_comment import DeleteComment
from blog.application.operations.write.edit_comment import EditComment
from blog.domain.comments.comment_id import CommentId
from blog.presentation.api.response_models import ErrorResponse, SuccessResponse

COMMENTS_ROUTER = APIRouter(prefix="/comments", tags=["comments"])


@COMMENTS_ROUTER.post(
    path="/",
    responses={
        HTTP_201_CREATED: {"model": SuccessResponse[CommentId]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_201_CREATED,
)
@inject
async def add_comment(
    request: AddComment,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[CommentId]:
    comment_id = await sender.send(request)
    return SuccessResponse(result=comment_id, status=HTTP_201_CREATED)


@COMMENTS_ROUTER.put(
    path="/{comment_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
        HTTP_403_FORBIDDEN: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def edit_comment(
    comment_id: CommentId,
    new_content: Annotated[str, Body()],
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(EditComment(new_content, comment_id))
    return SuccessResponse(status=HTTP_200_OK)


@COMMENTS_ROUTER.delete(
    path="/{comment_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
        HTTP_403_FORBIDDEN: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def delete_comment(
    comment_id: CommentId,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[None]:
    await sender.send(DeleteComment(comment_id))
    return SuccessResponse(status=HTTP_200_OK)


@COMMENTS_ROUTER.get(
    path="/{comment_id}",
    responses={
        HTTP_200_OK: {"model": SuccessResponse[CommentReadModel]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
    status_code=HTTP_200_OK,
)
@inject
async def get_comment(
    comment_id: CommentId,
    *,
    sender: FromDishka[Sender],
) -> SuccessResponse[CommentReadModel]:
    comment = await sender.send(GetCommentById(comment_id))
    return SuccessResponse(result=comment, status=HTTP_200_OK)
