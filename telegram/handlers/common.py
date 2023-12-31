from typing import Any

from aiogram import html
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, URLInputFile
from aiogram.utils.formatting import Text

import database as db
from api import api
from enums import Commands, SortOrder, ViewLimit


async def process_command_args(
    message: Message,
    command: CommandObject,
    state: FSMContext,
    next_state: State,
    args_len: int,
):
    query_params: dict[str, Any] = {"command": command.command}
    await state.set_data(query_params)
    if command.args is None:
        await message.answer("Please enter a product to search")
        await state.set_state(next_state)
        return False
    else:
        args = command.args.rsplit(" ", maxsplit=args_len - 1)
        if len(args) < args_len or args[0] == "":
            raise ValueError("Incorrect format. Please try again")
        else:
            return True


async def process_low_high_command(
    message: Message,
    command: CommandObject,
    state: FSMContext,
    next_state: State,
):
    process_args = False
    try:
        process_args = await process_command_args(
            message, command, state, next_state, args_len=2
        )

    except ValueError as exc:
        await message.answer(str(exc))
        return

    if command.args and process_args:
        query, limit_str = command.args.rsplit(" ", maxsplit=1)
        try:
            await process_search_query(query, state)
            await process_view_limit(limit_str, state)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await process_query(message, state)


async def process_search_query(search_query: str, state: FSMContext):
    search_query = search_query.strip()
    query_data = await state.get_data()
    query_data["query"] = search_query
    await state.set_data(query_data)


async def process_search_query_input(
    message: Message,
    state: FSMContext,
    next_state: State,
    next_state_message: Text,
):
    if message.text:
        await process_search_query(message.text, state)
        await state.set_state(next_state)
        await message.answer(**next_state_message.as_kwargs())


async def process_view_limit(limit_str: str, state: FSMContext):
    limit_str = limit_str.strip()
    if limit_str.isnumeric():
        limit = int(limit_str.strip())

        if ViewLimit.MIN.value <= limit <= ViewLimit.MAX.value:
            query_params = await state.get_data()
            query_params["limit"] = limit
            await state.set_data(query_params)
        else:
            raise ValueError(
                "Search results display limit should be in range"
                f" from {ViewLimit.MIN.value} to {ViewLimit.MAX.value}. "
                "Please try again"
            )
    else:
        raise ValueError("Search results display limit is incorrect. Please try again")


async def process_view_limit_input(message: Message, state: FSMContext):
    if message.text:
        try:
            await process_view_limit(message.text, state)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await process_query(message, state)


async def process_query(message: Message, state: FSMContext):
    query_params = await state.get_data()
    query = " ".join(str(param) for param in query_params.values())
    if message.from_user:
        user, created = db.User.get_or_create(
            user_id=message.from_user.id, first_name=message.from_user.first_name
        )

        db.History.create(
            query=f"{Commands.PREFIX}{query}",
            user=user,
        )

    await message.answer("Searching product...")
    match query_params["command"]:
        case Commands.LOW:
            sort_by = SortOrder.LOWEST_PRICE
        case Commands.HIGH:
            sort_by = SortOrder.HIGHEST_PRICE
        case _:
            sort_by = SortOrder.RELEVANCE
    results = await api.get_prices(
        query=query_params["query"],
        sort_by=sort_by,
        min_price=query_params.get("min_price"),
        max_price=query_params.get("max_price"),
    )
    if results:
        limit = query_params["limit"]
        results = results[:limit]
        await message.answer("Search results:")

        for result in results:
            title = result["product_title"]
            price = result["product_price"] or "Unavailable"
            link = result["product_url"]
            photo_url = result["product_photo"]
            photo = URLInputFile(photo_url)
            await message.answer_photo(
                photo,
                caption=f"{html.bold(title)}\nPrice: {price}\n{html.link(link, link)}",
                parse_mode=ParseMode.HTML,
            )
    else:
        await message.answer(
            "Results are not found.\n" "Please try different query of params"
        )
    await state.clear()
