# SPDX-FileCopyrightText: 2023-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT
from contextlib import contextmanager

import httpx
from attr import define
from attr import field

from .api_resources import SubscriberAPI


@define
class Listmonk:
    http_client: httpx.Client

    @property
    def subscribers(self) -> SubscriberAPI:
        return SubscriberAPI(self.http_client)


@contextmanager
def listmonk_session(app_url: str, user_login: str, user_pass: str) -> Listmonk:
    base_url = app_url + "/api"
    with httpx.Client(base_url=base_url, auth=(user_login, user_pass)) as http_client:
        yield Listmonk(http_client=http_client)
