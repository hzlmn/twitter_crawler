import json


class MainStorage:
    def __init__(self, redis):
        self.redis = redis

    async def get_settings(self):
        result = await self.redis.get("search_settings")
        if result is None:
            return
        return json.loads(result)

    async def create_settings(self, settings):
        return await self.redis.set("search_settings", json.dumps(settings))

    async def set_results(self, results):
        return await self.redis.lpush("search_results", json.dumps(results))

    async def get_results(self):
        results = await self.redis.lrange("search_results", 0, -1)
        if results is None:
            return
        return list(map(json.loads, results))
