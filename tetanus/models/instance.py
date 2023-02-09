from __future__ import annotations

from typing import Any

from ..types.http import InstancePayload


class Instance:
    def __init__(self, payload: InstancePayload):
        self._from_data(payload)

    def _from_data(self, payload: InstancePayload):
        self.instance_name: str = payload['instance_name']
        self.pandemonium_url: str = payload['pandemonium_url']
        self.oprish_url: str = payload['oprish_url']
        self.description: str = payload['description']
