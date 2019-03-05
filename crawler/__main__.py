import asyncio
import logging

from aiohttp import web

from .app import init_app

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = init_app(loop, "dev")
    web.run_app(app, port=8000)
