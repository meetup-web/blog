from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from blog.application.common.markers.command import Command
from blog.application.ports.identity_provider import IdentityProvider
from blog.domain.posts.factory import PostFactory
from blog.domain.posts.post_id import PostId
from blog.domain.posts.repository import PostRepository


@dataclass(frozen=True)
class CreatePost(Command[PostId]):
    title: str
    content: str


class CreatePostHandler(RequestHandler[CreatePost, PostId]):
    def __init__(
        self,
        post_factory: PostFactory,
        post_repository: PostRepository,
        identity_provider: IdentityProvider,
    ) -> None:
        self._post_factory = post_factory
        self._post_repository = post_repository
        self._identity_provider = identity_provider

    async def handle(self, request: CreatePost) -> PostId:
        current_user_id = self._identity_provider.current_user_id()
        post = self._post_factory.create(request.title, request.content, current_user_id)
        self._post_repository.add(post)

        return post.entity_id
