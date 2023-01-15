from uuid import UUID

import httpx
from attrs import define
from pendulum import DateTime

from py_listmonk.converter import converter

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum


    class StrEnum(str, Enum):
        pass


@define
class SubList:
    class Status(StrEnum):
        confirmed = "confirmed"
        unconfirmed = "unconfirmed"

    class Type(StrEnum):
        public = "public"
        private = "private"

    id: int
    subscription_status: Status
    uuid: UUID
    name: str
    type: Type
    tags: list[str]
    created_at: DateTime
    updated_at: DateTime


@define
class Subscriber:
    class Status(StrEnum):
        enabled = "enabled"
        disabled = "disabled"

    id: int
    uuid: str
    created_at: DateTime
    updated_at: DateTime
    email: str
    attribs: dict
    status: Status
    lists: list[SubList]


class SubscriberAPI:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    async def async_all(self) -> list[Subscriber]:
        response = await self.http_client.get("/subscribers")
        data = response.json()["data"]
        results = data["results"]
        return converter.structure(results, list[Subscriber])

    async def async_get(self, subscriber_id: int) -> Subscriber:
        response = await self.http_client.get(f"/subscribers/{subscriber_id}")
        data = response.json()["data"]
        return converter.structure(data, Subscriber)
