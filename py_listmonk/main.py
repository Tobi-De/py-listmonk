from functools import partial

import httpx
from dotenv import dotenv_values

from py_listmonk import Listmonk

config = dotenv_values(".env")

httpx_client = partial(
    httpx.Client,
    base_url=config["LISTMONK_APP_URL"],
    auth=(config["LISTMONK_USER_LOGIN"], config["LISTMONK_USER_PASS"]),
)

if __name__ == "__main__":
    with httpx_client() as http_client:
        listmonk = Listmonk(http_client=http_client)
        subs = listmonk.subscribers.all()
        print(listmonk.subscribers.get(subs[0].id))
