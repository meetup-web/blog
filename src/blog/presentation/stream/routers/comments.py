from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue, RabbitRouter

from blog.application.operations.write.delete_user_comments import DeleteUserComments
from blog.presentation.stream.request_models import UserDeleted

COMMENTS_ROUTER = RabbitRouter()


@COMMENTS_ROUTER.subscriber(
    RabbitQueue(
        name="user_delete_comments",
        routing_key="UserDeleted",
        auto_delete=False,
        durable=True,
    ),
    RabbitExchange(
        name="auth_exchange", type=ExchangeType.DIRECT, durable=True, auto_delete=False
    ),
    retry=True,
)
@inject
async def delete_user_comments(msg: UserDeleted, *, sender: FromDishka[Sender]) -> None:
    await sender.send(DeleteUserComments(user_id=msg.user_id))
