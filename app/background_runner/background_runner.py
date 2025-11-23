from abc import ABC, abstractmethod
from collections.abc import Callable
from pydoc import Doc
from typing import Annotated, Any, ParamSpec

P = ParamSpec("P")


class BackgroundRunner(ABC):
    @abstractmethod
    async def add_task(
        self,
        func: Annotated[
            Callable[P, Any],
            Doc(
                """
                The function to call after the response is sent.

                It can be a regular `def` function or an `async def` function.
                """
            ),
        ],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        raise NotImplementedError
