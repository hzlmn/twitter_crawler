import asyncio
from functools import partial

import aiohttp
from aiohttp import web
from yarl import URL

from .client import TwitterClient
from .handlers import MainHandler
from .helpers import get_config, setup_redis
from .middlewares import validation_middleware
from .router import setup_routes
from .settings import TWITTER_CLIENT_ID, TWITTER_CLIENT_SECRET
from .storages import MainStorage
from .tasks import fetch_twitter


async def on_shutdown(app):
    await app["client_session"].close()

    twitter_task = app.get("twitter_task")
    if twitter_task is not None:
        app["twitter_task"].cancel()

    app["redis"].close()
    await app["redis"].wait_closed()


async def init_app(loop, env):
    config = get_config(env)
    app = web.Application(middlewares=[validation_middleware])
    app["client_session"] = aiohttp.ClientSession()

    twitter_client = TwitterClient(app["client_session"],
                                   URL("https://api.twitter.com/"), config["timeout"])
    app["redis"] = await setup_redis(config)

    main_storage = MainStorage(app["redis"])
    main_handler = MainHandler(loop, twitter_client, main_storage)

    app = setup_routes(app, main_handler)

    access_token = (await twitter_client.get_token(
        TWITTER_CLIENT_ID,
        TWITTER_CLIENT_SECRET
    )).get("access_token")

    app["access_token"] = access_token

    app.on_shutdown.append(on_shutdown)

    return app
