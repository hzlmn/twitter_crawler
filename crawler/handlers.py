import logging
from functools import partial

from aiohttp import web

from .tasks import fetch_twitter
from .trafarets import (SettingsOutputTrafaret, SettingsTrafaret,
                        StatusesOutputTrafaret)

logger = logging.getLogger(__name__)


class MainHandler:
    def __init__(self, loop, twitter_client, storage):
        self.loop = loop
        self.twitter_client = twitter_client
        self.storage = storage

    async def get_settings(self, request):
        settings = await self.storage.get_settings()
        if settings is None:
            settings = {}
        resp = SettingsOutputTrafaret({"search_settings": settings})
        return web.json_response(resp)

    async def create_settings(self, request):
        post = await request.json()
        data = SettingsTrafaret(post)

        result = await self.storage.create_settings(data)

        if not result:
            raise web.HTTPBadRequest

        if request.app.get("twitter_task"):
            request.app["twitter_task"].cancel()

        request.app["twitter_task"] = self.loop.create_task(
            fetch_twitter(
                partial(self.twitter_client.search,
                        request.app["access_token"]),
                self.storage,
                data["search_phrase"],
                data["search_interval"],
            )
        )

        return web.Response(status=web.HTTPCreated.status_code)

    async def get_results(self, request):
        results = await self.storage.get_results()
        if results is None:
            raise web.HTTPNotFound
        return web.json_response(StatusesOutputTrafaret(results))
