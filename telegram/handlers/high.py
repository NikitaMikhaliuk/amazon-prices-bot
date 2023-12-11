from aiogram import F, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.formatting import Text

from enums import Commands

from .common import (
    process_low_high_command,
    process_search_query_input,
    process_view_limit_input,
)


class SearchHighPrices(StatesGroup):
    input_query = State()
    input_view_limit = State()


router = Router()


@router.message(StateFilter(None), Command(Commands.HIGH))
async def high_command(message: Message, command: CommandObject, state: FSMContext):
    await process_low_high_command(
        message, command, state, next_state=SearchHighPrices.input_query
    )


@router.message(StateFilter(SearchHighPrices.input_query), F.text)
async def input_search_query(message: Message, state: FSMContext):
    await process_search_query_input(
        message,
        state,
        next_state=SearchHighPrices.input_view_limit,
        next_state_message=Text("Введите кол-во отображаемых результатов"),
    )


@router.message(StateFilter(SearchHighPrices.input_view_limit), F.text)
async def input_view_limit(message: Message, state: FSMContext):
    await process_view_limit_input(message, state)
