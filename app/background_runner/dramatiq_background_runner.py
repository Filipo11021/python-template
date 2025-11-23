from __future__ import annotations

import importlib
import inspect
import json
from collections.abc import Callable
from typing import Annotated, Any, ParamSpec, get_args, get_origin

import dramatiq

from app.background_runner.background_runner import BackgroundRunner

P = ParamSpec("P")


def _get_function_path(func: Callable[..., Any]) -> str:
    return f"{func.__module__}.{func.__qualname__}"


def _get_function_from_path(path: str) -> Callable[..., Any]:
    module_path, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def _get_fastapi_dep_from_annotation(annotation: Any) -> Any | None:
    if get_origin(annotation) is not Annotated:
        return None

    for metadata in get_args(annotation):
        if hasattr(metadata, "dependency") and callable(metadata.dependency):
            return metadata.dependency()

    return None


def _resolve_fastapi_deps(
    func: Callable[..., Any], kwargs: dict[str, Any]
) -> dict[str, Any]:
    resolved = kwargs.copy()
    signature = inspect.signature(func)

    for name, param in signature.parameters.items():
        if name in resolved:
            continue

        fastapi_dep = _get_fastapi_dep_from_annotation(param.annotation)
        if fastapi_dep is not None:
            resolved[name] = fastapi_dep

    return resolved


@dramatiq.actor(actor_name="task_dispatcher")
def _task_dispatcher(fn_path: str, args: list[Any], kwargs: dict[str, Any]) -> Any:
    func = _get_function_from_path(fn_path)
    resolved_kwargs = _resolve_fastapi_deps(func, kwargs)
    return func(*args, **resolved_kwargs)


def _get_json_serializable_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    serializable_kwargs = {}
    for key, value in kwargs.items():
        try:
            json.dumps(value)
            serializable_kwargs[key] = value
        except (TypeError, ValueError):
            continue
    return serializable_kwargs


class DramatiqBackgroundRunner(BackgroundRunner):
    def __init__(self, broker: dramatiq.Broker, queue: str = "default") -> None:
        self.broker = broker
        self.queue = queue

    async def add_task(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        fn_path = _get_function_path(func)
        serializable_kwargs = _get_json_serializable_kwargs(kwargs)

        message = _task_dispatcher.message_with_options(
            args=(fn_path, list(args), serializable_kwargs),
            queue_name=self.queue,
        )

        self.broker.enqueue(message)
