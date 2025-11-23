import asyncio
from dataclasses import dataclass

import dramatiq
from dramatiq.brokers.stub import StubBroker

from app.background_runner.dramatiq_background_runner import (
    DramatiqBackgroundRunner,
    _task_dispatcher,
)
from tests.integrations.background_runner.background_runner_context import (
    BackgroundRunnerContext,
)


@dataclass
class DramatiqBackgroundRunnerContext(BackgroundRunnerContext):
    runner: DramatiqBackgroundRunner
    broker: StubBroker

    def get_enqueued_count(self, queue: str = "default") -> int:
        return self.broker.queues[queue].qsize()

    async def process_enqueued_jobs(self, queue: str = "default") -> None:
        self.broker.add_middleware(dramatiq.middleware.CurrentMessage())
        self.broker.declare_actor(_task_dispatcher)
        worker = dramatiq.Worker(self.broker, worker_threads=1)
        worker.start()
        try:
            await asyncio.to_thread(self.broker.join, queue)
            worker.join()
        finally:
            worker.stop()


def make_dramatiq_context() -> BackgroundRunnerContext:
    broker = StubBroker()
    broker.declare_queue("default")
    dramatiq.set_broker(broker)
    runner = DramatiqBackgroundRunner(broker)
    return DramatiqBackgroundRunnerContext(runner, broker)
