from __future__ import annotations
import asyncio

from typing import Any, Callable, Coroutine, TypeVar

from collections import defaultdict

import inspect

from .http import HTTPClient

from ..types.gateway import MessageData
from ..models.message import Message

T = TypeVar("T")
Func = Callable[..., T]
CoroFunc = Func[Coroutine[Any, Any, Any]]

class Dispatcher:
    def __init__(self, http: HTTPClient):
        self.http = http
        self.events: dict[str, list[CoroFunc]] = defaultdict(list)

    def add_callback(self, event_name: str, func: CoroFunc) -> None:
        self.events[event_name].append(func)

    def subscribe(self, event_name: str, func: CoroFunc):
        self.add_callback(event_name, func)

    def get_event(self, event_name: str):
        return self.events.get(event_name)

    def dispatch(self, event_name: str, *args, **kwargs):
        event = self.get_event(event_name)

        if event is None:
            return

        for callback in event:
            asyncio.create_task(callback(*args, **kwargs))