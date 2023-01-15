import pytest

from py_listmonk import Listmonk
from py_listmonk.api_resources import Subscriber


@pytest.mark.asyncio
async def test_subscribers_all(listmonk: Listmonk):
    res = await listmonk.subscribers.async_all()
    assert isinstance(res[0], Subscriber)


@pytest.mark.asyncio
async def test_subscribers_get(listmonk: Listmonk):
    res = await listmonk.subscribers.async_all()
    res = await listmonk.subscribers.async_get(res[0].id)
    assert isinstance(res, Subscriber)
