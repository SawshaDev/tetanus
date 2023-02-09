from __future__ import annotations

import asyncio
import inspect
import json
from logging import getLogger
from typing import Any, Callable, Optional, cast

from aiohttp import ClientWebSocketResponse, WSMessage

from ..models.message import Message
from ..types.gateway import GatewayData, MessageData
from .dispatcher import Dispatcher
from .http import HTTPClient

_log = getLogger(__name__)


class OPCodes:
    MESSAGE_CRREATE = "MESSAGE_CREATE"
    PING = "PING"
    PONG = "PONG"


class GatewayClient:
    def __init__(self, http: HTTPClient, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self._http = http
        self.ws: Optional[ClientWebSocketResponse] = None
        self.first_ping: bool = True

    async def receive(self):
        if not self.ws:
            return

        msg: WSMessage = await self.ws.receive()

        self.recent_payload = cast(GatewayData, msg.json())

        return True

    async def keep_connection(self):
        if not self.ws:
            return

        await self.ws.send_json({"op": OPCodes.PING})

        await asyncio.sleep(45.0)

        asyncio.create_task(self.keep_connection())

    async def connect(self):
        gateway_url = (await self._http.fetch_instance()).pandemonium_url

        self.ws = await self._http._session.ws_connect(gateway_url)

        _log.info(f"Successfully connected to eludris gateway")
        _log.info("Sent first ping payload to gateway")
        asyncio.create_task(self.keep_connection())

        return await self.listen_for_events()

    async def listen_for_events(self):
        if not self.ws:
            return

        while not self.ws.closed:
            res = await self.receive()

            if res and self.recent_payload is not None:
                op = self.recent_payload["op"]
                data = self.recent_payload.get("d")

                if op.lower() not in self.dispatcher.events.keys():
                    continue

                if op == "MESSAGE_CREATE":
                    msg_data = cast(MessageData, data)

                    message = Message(msg_data)

                    self.dispatcher.dispatch(op.lower(), message)

    async def close(self) -> None:
        if not self.ws:
            return

        if not self.ws.closed:
            await self.ws.close()

            _log.info("Disconnected from gateway")
