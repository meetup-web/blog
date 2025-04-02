from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue, RabbitRouter

from blog.application.operations.write.delete_user_posts import DeleteUserPosts
from blog.presentation.stream.request_models import UserDeleted

POSTS_ROUTER = RabbitRouter()


@POSTS_ROUTER.subscriber(
    RabbitQueue(
        name="user_delete_posts",
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
    await sender.send(DeleteUserPosts(user_id=msg.user_id))
