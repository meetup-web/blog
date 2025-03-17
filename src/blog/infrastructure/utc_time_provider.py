from datetime import UTC, datetime

from blog.application.ports.time_provider import TimeProvider


class UtcTimeProvider(TimeProvider):
    def provide_current(self) -> datetime:
        return datetime.now(UTC)
