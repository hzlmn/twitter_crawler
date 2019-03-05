import asyncio
import time
from collections import Counter

from .algos import filter_urls, most_common, most_used_phrase


async def fetch_twitter(handler, storage, query, interval):
    # Search interval interpreted as second between requests.
    # 0 means script is currently stopped
    while interval:
        timestamp = int(time.time())
        result = await handler(query)

        statuses = result.get("statuses", [])

        twits = []
        user_ids = []
        hashtags = []
        for status in result.get("statuses", []):
            twits.append(filter_urls(status["text"]))
            user_ids.append(status["user"]["id_str"])
            tags = status["entities"].get("hashtags", [])
            for tag in tags:
                hashtags.append(tag.get("text"))

        top_phrase = most_used_phrase(" ".join(twits))
        top_publisher = most_common(user_ids)[0]
        top_hashtags = most_common(hashtags, count=3)

        results = {
            "executed_at": timestamp,
            "interval": interval,
            "search_phrase": query,
            "statistics": {
                "top_hashtags": top_hashtags,
                "top_phrase": top_phrase,
                "top_publisher": top_publisher,
                "tweet_count": len(result.get("statuses", []))
            }
        }

        print(results)

        await storage.set_results(results)

        await asyncio.sleep(interval)
