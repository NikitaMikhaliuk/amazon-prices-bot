from aiogram import F, Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.formatting import Text

from enums import Commands

from .common import (
    process_command_args,
    process_query,
    process_search_query,
    process_search_query_input,
    process_view_limit,
    process_view_limit_input,
)


class SearchCustomPrices(StatesGroup):
    input_query = State()
    input_view_limit = State()
    input_min_price = State()
    input_max_price = State()


router = Router()


@router.message(StateFilter(None), Command(Commands.CUSTOM))
async def custom_command(message: Message, command: CommandObject, state: FSMContext):
    process_args = False
    try:
        process_args = await process_command_args(
            message,
            command,
            state,
            next_state=SearchCustomPrices.input_query,
            args_len=4,
        )

    except ValueError as exc:
        await message.answer(str(exc))
        return

    if command.args and process_args:
        query, min_price_str, max_price_str, limit_str = command.args.rsplit(
            " ", maxsplit=3
        )
        try:
            await process_search_query(query, state)
            await process_view_limit(limit_str, state)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await process_query(message, state)


@router.message(StateFilter(SearchCustomPrices.input_query), F.text)
async def input_search_query(message: Message, state: FSMContext):
    await process_search_query_input(
        message,
        state,
        next_state=SearchCustomPrices.input_min_price,
        next_state_message=Text("Введите минимальную цену"),
    )


@router.message(StateFilter(SearchCustomPrices.input_min_price), F.text)
async def input_min_price(message: Message, state: FSMContext):
    if message.text:
        min_price_str = message.text.strip()

        if min_price_str.isnumeric():
            min_price = int(min_price_str.strip())

            if min_price > 0:
                query_params = await state.get_data()
                query_params["min_price"] = min_price
                await state.set_data(query_params)
                await message.answer("Введите максимальную цену")
                await state.set_state(SearchCustomPrices.input_max_price)
            else:
                await message.answer(
                    "Минимальная цена не может быть меньше 0. "
                    "Попробуйте ввести снова"
                )
        else:
            await message.answer(
                "Неверно указана минимальная цена. Попробуйте ввести снова"
            )


@router.message(StateFilter(SearchCustomPrices.input_max_price), F.text)
async def input_max_price(message: Message, state: FSMContext):
    if message.text:
        query_params = await state.get_data()
        max_price_str = message.text.strip()
        if max_price_str.isnumeric():
            max_price = int(max_price_str.strip())

            if max_price > query_params["min_price"]:
                query_params["max_price"] = max_price
                await state.set_data(query_params)
                await message.answer("Введите кол-во отображаемых результатов")
                await state.set_state(SearchCustomPrices.input_view_limit)
            else:
                await message.answer(
                    "Максимальная цена не может быть меньше минимальной. "
                    "Попробуйте ввести снова"
                )
        else:
            await message.answer(
                "Неверно указана максимальной цена. Попробуйте ввести снова"
            )


@router.message(StateFilter(SearchCustomPrices.input_view_limit), F.text)
async def input_view_limit(message: Message, state: FSMContext):
    await process_view_limit_input(message, state)
