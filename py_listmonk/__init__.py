# SPDX-FileCopyrightText: 2023-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from contextlib import contextmanager, asynccontextmanager

import httpx
from attr import define

from .api_resources import SubscriberAPI
from .async_to_sync import sync_await


@define
class Listmonk:
    http_client: httpx.AsyncClient

    @property
    def subscribers(self) -> SubscriberAPI:
        return SubscriberAPI(self.http_client)


@contextmanager
def listmonk_session(base_url: str, login: str, password: str):
    http_client = httpx.AsyncClient(base_url=base_url, auth=(login, password))
    yield Listmonk(http_client)
    sync_await(http_client.aclose())


@asynccontextmanager
async def listmonk_session_async(base_url: str, login: str, password: str):
    async with httpx.AsyncClient(
            base_url=base_url, auth=(login, password)
    ) as http_client:
        yield Listmonk(http_client)
