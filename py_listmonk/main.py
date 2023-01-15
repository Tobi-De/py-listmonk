import asyncio
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


async def main():
    async with httpx_client() as client:
        listmonk = Listmonk(client)
        subs = await listmonk.subscribers.async_all()
        print(await listmonk.subscribers.async_get(subs[0].id))


if __name__ == "__main__":
    asyncio.run(main())
