import asyncio
import logging

from telegram.bot import start_bot


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
