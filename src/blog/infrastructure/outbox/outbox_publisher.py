from abc import ABC, abstractmethod

from blog.infrastructure.outbox.outbox_message import OutboxMessage


class OutboxPublisher(ABC):
    @abstractmethod
    async def publish(self, message: OutboxMessage) -> None: ...
