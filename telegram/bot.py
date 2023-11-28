from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# Доп. импорт для раздела про стратегии FSM
from aiogram.fsm.strategy import FSMStrategy

from settings import config

from .handlers import hello_world


async def start_bot():
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

    dp.include_router(hello_world.router)
    # dp.include_routers(...)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
