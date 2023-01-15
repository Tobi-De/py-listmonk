import asyncio

import httpx
from pytest_asyncio import fixture

from py_listmonk import Listmonk


@fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
async def listmonk():
    async with httpx.AsyncClient(base_url="http://localhost:9000/api") as client:
        yield Listmonk(client)
