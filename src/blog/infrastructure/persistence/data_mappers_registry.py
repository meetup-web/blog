from abc import ABC, abstractmethod

from blog.domain.shared.entity import Entity
from blog.infrastructure.persistence.data_mapper import DataMapper


class DataMappersRegistry(ABC):
    @abstractmethod
    def get_mapper(self, entity: type[Entity]) -> DataMapper: ...
