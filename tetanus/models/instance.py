from __future__ import annotations

from ..types.http import InstancePayload


class Instance:
    def __init__(self, payload: InstancePayload):
        self._from_data(payload)

    def _from_data(self, payload: InstancePayload):
        self.instance_name = payload['instance_name']
        self.pandemonium_url = payload['pandemonium_url']
        self.oprish_url = payload['oprish_url']
        self.description = payload['description']