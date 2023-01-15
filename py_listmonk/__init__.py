# SPDX-FileCopyrightText: 2023-present Tobi DEGNON <tobidegnon@proton.me>
#
# SPDX-License-Identifier: MIT

import httpx
from attr import define

from .api_resources import SubscriberAPI


@define
class Listmonk:
    http_client: httpx.AsyncClient

    @property
    def subscribers(self) -> SubscriberAPI:
        return SubscriberAPI(self.http_client)
