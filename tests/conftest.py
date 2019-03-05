import asyncio

import pytest

from crawler.app import init_app
from crawler.helpers import get_config, setup_redis


@pytest.fixture
def config():
    return get_config("test")


@pytest.fixture
async def redis(config):
    redis = await setup_redis(config)
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
def flush_redis(redis):
    return redis.flushall


@pytest.fixture
async def client(loop, flush_redis, aiohttp_client):
    await flush_redis()
    loop = asyncio.get_event_loop()
    app = await init_app(loop, env="test")
    client = await aiohttp_client(app)
    return client
