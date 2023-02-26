from __future__ import annotations

from typing import Any, Optional
from urllib.parse import quote as urlquote

from aiohttp import ClientSession

from ..errors import HTTPException
from ..models import Instance
from ..types.http import InstancePayload
from ..types.gateway import MessageData


class Route:
    def __init__(self, method: str, url: str, **params: Any) -> None:
        self.params: dict[str, Any] = params
        self.method: str = method
        self.url: str = url

    @property
    def endpoint(self) -> str:
        """The formatted url for this route."""
        return self.url.format_map({k: urlquote(str(v)) for k, v in self.params.items()})


class HTTPClient:
    def __init__(self, api_url: str):
        self.url = api_url


    async def login(self):
        self._session = ClientSession()

    async def request(self, route: Route, *, json: Optional[dict[str, Any]] = None) -> Any:
        resp = await self._session.request(route.method, f"{self.url}{route.url}", json=json)

        if 200 <= resp.status < 300:
            return await resp.json()

        if resp.status >= 400:
            raise HTTPException(resp, await resp.json())

    async def fetch_instance(self) -> Instance:
        payload: InstancePayload = await self.request(Route("GET", "/"))

        return Instance(payload)

    async def send_message(self, author: str, content: str) -> MessageData:
        payload: MessageData = await self.request(Route("POST", "/messages"), json={"author": author, "content": content})

        return payload