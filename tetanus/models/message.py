from __future__ import annotations

from typing import Any

from ..types.gateway import MessageData


class Message:
    def __init__(self, payload: MessageData):
        self._from_data(payload)

    def _from_data(self, payload: MessageData):
        self.content = payload['content']
        self.author = payload['author']
