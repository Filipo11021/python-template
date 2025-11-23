from abc import ABC, abstractmethod

from app.background_runner.background_runner import BackgroundRunner


class BackgroundRunnerContext(ABC):
    runner: BackgroundRunner

    @abstractmethod
    def get_enqueued_count(self, queue: str = "default") -> int:
        pass

    @abstractmethod
    async def process_enqueued_jobs(self, queue: str = "default") -> None:
        pass
