import asyncio

from aiohttp import web


async def test_get_settings(client):
    resp = await client.get("/search_settings")
    assert resp.status == web.HTTPOk.status_code
    result = await resp.json()
    assert result == {"search_settings": {}}


async def test_create_settings(client):
    resp = await client.get("/search_settings")
    assert resp.status == web.HTTPOk.status_code
    result = await resp.json()
    assert result == {"search_settings": {}}

    resp = await client.post("/search_settings", json={
        "search_phrase": "test",
        "search_interval": 3
    })
    assert resp.status == web.HTTPCreated.status_code

    resp = await client.get("/search_settings")
    assert resp.status == web.HTTPOk.status_code
    result = await resp.json()
    assert result == {"search_settings": {
        "search_phrase": "test",
        "search_interval": 3,
    }}


async def test_get_results(client):
    resp = await client.get("/search_settings")
    result = await resp.json()
    assert result == {"search_settings": {}}

    resp = await client.post("/search_settings", json={
        "search_phrase": "Machine Learning",
        "search_interval": 3,
    })
    assert resp.status == web.HTTPCreated.status_code

    await asyncio.sleep(3)

    results = await client.get("/seach_results")
    assert results
