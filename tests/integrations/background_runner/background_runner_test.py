from typing import Annotated

from fastapi import Depends

from tests.integrations.background_runner.background_runner_context import (
    BackgroundRunnerContext,
)


class NonSerializable:
    pass


def sample_function(a: int, b: str) -> str:
    return f"{a}-{b}"


async def test_add_task_filters_non_serializable_kwargs(
    runner_ctx: BackgroundRunnerContext,
) -> None:
    non_serializable_obj = NonSerializable()

    await runner_ctx.runner.add_task(
        sample_function,
        42,
        b="test",
        invalid=non_serializable_obj,  # type: ignore[call-arg]
    )

    assert runner_ctx.get_enqueued_count() == 1


async def test_end_to_end_task_execution(runner_ctx: BackgroundRunnerContext) -> None:
    await runner_ctx.runner.add_task(sample_function, 999, b="end-to-end")

    assert runner_ctx.get_enqueued_count() == 1

    await runner_ctx.process_enqueued_jobs()

    assert runner_ctx.get_enqueued_count() == 0


class DatabaseConnection:
    def __init__(self, host: str):
        self.host = host
        self._connection = object()

    def execute(self) -> str:
        return "Executed successfully"


def get_database_connection() -> DatabaseConnection:
    return DatabaseConnection("localhost")


def process_order(
    order_id: int, db: Annotated[DatabaseConnection, Depends(get_database_connection)]
) -> str:
    result = db.execute()
    return f"Order {order_id} processed: {result}"


async def test_with_non_serializable_fastapi_dependency(
    runner_ctx: BackgroundRunnerContext,
) -> None:
    await runner_ctx.runner.add_task(process_order, 42, db=get_database_connection())

    assert runner_ctx.get_enqueued_count() == 1

    await runner_ctx.process_enqueued_jobs()

    assert runner_ctx.get_enqueued_count() == 0
