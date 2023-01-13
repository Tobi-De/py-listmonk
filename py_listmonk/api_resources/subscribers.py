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


class SubscriberAPI:
    def __init__(self, http_client: httpx.Client):
        self.http_client = http_client

    def all(self) -> list[Subscriber]:
        response = self.http_client.get("/subscribers")
        data = response.json()["data"]
        results = data["results"]
        return converter.structure(results, list[Subscriber])

    def get(self, subscriber_id: int) -> Subscriber:
        response = self.http_client.get(f"/subscribers/{subscriber_id}")
        data = response.json()["data"]
        return converter.structure(data, Subscriber)
