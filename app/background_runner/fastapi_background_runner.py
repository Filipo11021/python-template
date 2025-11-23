from collections.abc import Callable
from typing import Any, ParamSpec

from fastapi import BackgroundTasks

from app.background_runner.background_runner import BackgroundRunner

P = ParamSpec("P")


class FastapiBackgroundRunner(BackgroundRunner):
    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.background_tasks = background_tasks

    async def add_task(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self.background_tasks.add_task(func, *args, **kwargs)
