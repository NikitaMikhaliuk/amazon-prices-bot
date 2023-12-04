from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy

from settings import config

from .handlers import custom, high, low


async def start_bot():
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

    # dp.include_router(hello_world.router)
    dp.include_routers(
        low.router,
        high.router,
        custom.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
