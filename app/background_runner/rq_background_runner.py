from collections.abc import Callable
from typing import Any, ParamSpec

from redis import Redis
from rq import Queue

from app.background_runner.background_runner import BackgroundRunner

P = ParamSpec("P")


class RQBackgroundRunner(BackgroundRunner):
    def __init__(self, connection: Redis, queue_name: str = "default") -> None:
        self.rq = Queue(name=queue_name, connection=connection)

    async def add_task(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self.rq.enqueue(func, *args, **kwargs)
