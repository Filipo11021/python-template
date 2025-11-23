from typing import Annotated

import dramatiq
from fastapi import Depends

from app.background_runner.background_runner import BackgroundRunner
from app.background_runner.dramatiq_background_runner import DramatiqBackgroundRunner


def get_background_runner() -> BackgroundRunner:
    return DramatiqBackgroundRunner(broker=dramatiq.get_broker(), queue="default")


BackgroundRunnerDep = Annotated[BackgroundRunner, Depends(get_background_runner)]
