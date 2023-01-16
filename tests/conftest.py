import asyncio

from pytest_asyncio import fixture

from py_listmonk import listmonk_session_async


@fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
async def listmonk():
    async with listmonk_session_async(
            base_url="http://localhost:9000/api", password="", login=""
    ) as client:
        yield client
