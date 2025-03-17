from blog.domain.comments.comment import Comment
from blog.domain.posts.post import Post
from blog.domain.shared.entity import Entity
from blog.infrastructure.persistence.adapters.sql_comment_data_mapper import (
    SqlCommentDataMapper,
)
from blog.infrastructure.persistence.adapters.sql_post_data_mapper import (
    SqlPostDataMapper,
)
from blog.infrastructure.persistence.data_mapper import DataMapper
from blog.infrastructure.persistence.data_mappers_registry import (
    DataMappersRegistry,
)


class SqlDataMappersRegistry(DataMappersRegistry):
    def __init__(
        self,
        post_data_mapper: SqlPostDataMapper,
        comment_data_mapper: SqlCommentDataMapper,
    ) -> None:
        self._data_mappers_map: dict[type[Entity], DataMapper] = {
            Post: post_data_mapper,
            Comment: comment_data_mapper,
        }

    def get_mapper[EntityT: Entity](self, entity: type[EntityT]) -> DataMapper[EntityT]:
        mapper = self._data_mappers_map.get(entity)

        if not mapper:
            raise KeyError(f"DataMapper for {entity.__name__!r} not registered")

        return mapper
