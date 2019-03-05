import logging
import os
from pathlib import Path

import aioredis
import yaml

from .settings import PROJECT_ROOT

logger = logging.getLogger(__name__)


def get_config(env):
    with Path(PROJECT_ROOT / "configs" / f"{env}.yml").open() as fp:
        return yaml.load(fp.read())


async def setup_redis(config):
    return await aioredis.create_redis(f"redis://{config['redis_host']}:{config['redis_port']}")


def required_env(variable):
    result = os.environ.get(variable)
    if result is None:
        raise RuntimeError(f"{variable} is required for running system")
    return result
