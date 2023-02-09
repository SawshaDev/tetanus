from __future__ import annotations

from typing import TypedDict


class InstancePayload(TypedDict):
    instance_name: str
    description: str
    version: str
    message_limit: int
    oprish_url: str
    pandemonium_url: str
    effis_url: str
    file_size: int
    attachment_file_size: int
