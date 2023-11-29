import asyncio
import logging
import os

import database as db
from settings import config
from telegram.bot import start_bot


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    if not os.path.exists(config.database):
        db.create_tables()
    else:
        db.connect()

    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
