import asyncio
from functools import partial

import httpx
from dotenv import dotenv_values

from py_listmonk import listmonk_session, listmonk_session_async

config = dotenv_values(".env")

httpx_client = partial(
    httpx.AsyncClient,
    base_url=config["LISTMONK_APP_URL"],
    auth=(config["LISTMONK_USER_LOGIN"], config["LISTMONK_USER_PASS"]),
)


async def main():
    async with listmonk_session_async(
            base_url=config["LISTMONK_APP_URL"],
            login=config["LISTMONK_USER_LOGIN"],
            password=config["LISTMONK_USER_PASS"],
    ) as listmonk:
        subs = await listmonk.subscribers.all_async()
        print(await listmonk.subscribers.get_async(subs[0].id))


def sync_main():
    with listmonk_session(
            base_url=config["LISTMONK_APP_URL"],
            login=config["LISTMONK_USER_LOGIN"],
            password=config["LISTMONK_USER_PASS"],
    ) as listmonk:
        subs = listmonk.subscribers.all()
        print(listmonk.subscribers.get(subs[0].id))


if __name__ == "__main__":
    # sync_main()
    asyncio.run(main())
