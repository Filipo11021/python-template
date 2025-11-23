from collections.abc import AsyncGenerator

import pytest

from tests.integrations.background_runner.background_runner_context import (
    BackgroundRunnerContext,
)
from tests.integrations.background_runner.dramatiq import make_dramatiq_context
from tests.integrations.background_runner.fastapi_background_tasks import (
    make_fastapi_context,
)
from tests.integrations.background_runner.rq import make_rq_context


@pytest.fixture(
    params=[make_dramatiq_context, make_rq_context, make_fastapi_context],
    ids=["dramatiq", "rq", "fastapi"],
)
async def runner_ctx(
    request: pytest.FixtureRequest,
) -> AsyncGenerator[BackgroundRunnerContext]:
    ctx = request.param()
    yield ctx
