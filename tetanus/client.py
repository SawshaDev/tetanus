from __future__ import annotations

import asyncio

from .impl.dispatcher import Dispatcher
from .impl.gateway import GatewayClient
from .impl.http import HTTPClient

from .models import Message

DEFAULT_API_URL = "https://api.eludris.gay"

class Client:
    def __init__(self, name: str, api_url: str = DEFAULT_API_URL):
        self.name = name
        self.http = HTTPClient(api_url)


        self.loop = asyncio.get_event_loop()
        self.dispatcher = Dispatcher(self.http)

    def listen(self, name: str):
        def inner(func):
            if name not in self.dispatcher.events:
                self.dispatcher.subscribe(name, func)
            else:
                self.dispatcher.add_callback(name, func)

        return inner

    def subscribe(self, event: str, func):
        self.dispatcher.subscribe(event, func)

    async def login(self):
        await self.http.login()

    async def connect(self):
        self.gateway = GatewayClient(self.http, self.dispatcher)

        while True:
            await self.gateway.connect()

    async def create_message(self, content: str) -> Message:
        payload = await self.http.send_message(self.name, content)

        return Message(payload)

    async def start(self):
        await self.login()
        await self.connect()

    async def close(self):
        if not self.gateway or not self.http:
            return

        await self.gateway.close()
        await self.http._session.close()

    def run(self):
        try:
            asyncio.run(self.start())
        except (KeyboardInterrupt, RuntimeError):
            self.loop.run_until_complete(self.close())
