from dataclasses import dataclass

from fastapi import BackgroundTasks

from app.background_runner.fastapi_background_runner import FastapiBackgroundRunner
from tests.integrations.background_runner.background_runner_context import (
    BackgroundRunnerContext,
)


@dataclass
class FastapiBackgroundRunnerContext(BackgroundRunnerContext):
    runner: FastapiBackgroundRunner
    background_tasks: BackgroundTasks

    def get_enqueued_count(self, queue: str = "default") -> int:
        return len(self.background_tasks.tasks)

    async def process_enqueued_jobs(self, queue: str = "default") -> None:
        for task in self.background_tasks.tasks:
            await task()
            self.background_tasks.tasks.remove(task)


def make_fastapi_context() -> BackgroundRunnerContext:
    background_tasks = BackgroundTasks()
    runner = FastapiBackgroundRunner(background_tasks)
    return FastapiBackgroundRunnerContext(runner, background_tasks)
