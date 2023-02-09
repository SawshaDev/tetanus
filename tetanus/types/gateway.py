from __future__ import annotations

from typing import Optional, TypedDict


class GatewayData(TypedDict):
    op: str
    d: Optional[str]


class MessageData(TypedDict):
    author: str
    content: str
