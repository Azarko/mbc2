import pytest

from mbc2 import main


@pytest.fixture
async def web_app_client(aiohttp_client):
    client = await aiohttp_client(await main.create_app())
    yield client
