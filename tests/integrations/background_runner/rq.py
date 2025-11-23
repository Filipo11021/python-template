from dataclasses import dataclass

from fakeredis import FakeRedis
from redis import Redis
from rq import Queue, SimpleWorker

from app.background_runner.rq_background_runner import RQBackgroundRunner
from tests.integrations.background_runner.background_runner_context import (
    BackgroundRunnerContext,
)


@dataclass
class RQBackgroundRunnerContext(BackgroundRunnerContext):
    runner: RQBackgroundRunner
    connection: Redis

    def get_enqueued_count(self, queue: str = "default") -> int:
        q = Queue(name=queue, connection=self.connection)
        return q.count

    async def process_enqueued_jobs(self, queue: str = "default") -> None:
        worker = SimpleWorker([queue], connection=self.connection)
        worker.work(burst=True)


def make_rq_context() -> BackgroundRunnerContext:
    connection = FakeRedis()
    runner = RQBackgroundRunner(connection=connection)
    return RQBackgroundRunnerContext(runner=runner, connection=connection)
