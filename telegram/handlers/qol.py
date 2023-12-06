from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

import database as db
from enums import Commands


class SearchLowPrices(StatesGroup):
    input_query = State()
    input_view_limit = State()


router = Router()


@router.message(StateFilter(None), Command(Commands.HISTORY))
async def history_command(message: Message):
    if message.from_user:
        history = db.get_user_last_queries(message.from_user.id)

        if history:
            await message.answer("Ваши последние запросы:")
            for entry in history:
                await message.answer(entry.query)
        else:
            await message.answer("Ваша история запросов пуста")
