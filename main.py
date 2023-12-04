import asyncio
import logging
import os

from icecream import install

import database as db
from api import api
from settings import config
from telegram.bot import start_bot


def main():
    install()
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    if not os.path.exists(config.database):
        db.create_tables()
    else:
        db.connect()

    asyncio.run(start_bot())


async def exit():
    print("Exit")
    await api.destroy()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        asyncio.run(exit())
