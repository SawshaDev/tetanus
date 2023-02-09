from __future__ import annotations

from typing import Any, Optional
from urllib.parse import quote as urlquote

from aiohttp import ClientResponse, ClientSession

import json

from ..models.instance import Instance
from ..types.http import InstancePayload
from ..errors import HTTPException

DEFAULT_URL = "https://api.eludris.gay"


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
    def __init__(self, api_url: Optional[str] = None):
        if api_url is None:
            self.url = DEFAULT_URL
        else:
            self.url = api_url
            
        self._session: ClientSession = None  # type: ignore

    @staticmethod
    async def _text_or_json(resp: ClientResponse) -> dict[str, Any]:
        text = await resp.text()

        if resp.content_type == "application/json":
            return json.loads(text)

        return text  # type: ignore

    async def login(self):
        self._session = ClientSession()

    async def request(self, route: Route, *, json: Optional[dict[str, Any]] = None) -> Any:
        resp = await self._session.request(route.method, f"{self.url}{route.url}", json=json)

        if 200 <= resp.status < 300:
            return await self._text_or_json(resp)

        if resp.status >= 400:
            raise HTTPException(resp, await self._text_or_json(resp))
        
    async def fetch_instance(self) -> Instance:
        payload: InstancePayload = await self.request(Route("GET", "/"))

        return Instance(payload)