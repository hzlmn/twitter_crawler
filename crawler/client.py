import asyncio
from functools import partialmethod

import aiohttp
import async_timeout
from yarl import URL


class BaseClient:
    def __init__(self, session, base_url, timeout):
        self.client_session = session
        self.timeout = timeout
        self.base_url = URL(base_url)

    async def request(self, method, part, base_url=None, **kwargs):
        if base_url is not None:
            url = URL(base_url) / part
        else:
            url = self.base_url / part

        async with async_timeout.timeout(self.timeout):
            async with self.client_session.request(method, url, **kwargs) as resp:
                if "application/json" in resp.headers["Content-Type"]:
                    return await resp.json()

                return await resp.text()

    get = partialmethod(request, "GET")

    post = partialmethod(request, "POST")


class TwitterClient(BaseClient):
    async def get_token(self, client_id, client_secret):
        result = await self.post(
            f"oauth2/token",
            auth=aiohttp.BasicAuth(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        )
        return result or {}

    async def search(self, access_token, query, version="1.1", count=10):
        result = await self.get(
            f"{version}/search/tweets.json",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"q": query, "count": count},
        )

        return result
