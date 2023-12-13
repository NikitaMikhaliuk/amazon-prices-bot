from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.formatting import Bold, Italic, Text, TextLink

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
            await message.answer("Your last queries:")
            for entry in history:
                await message.answer(entry.query)
        else:
            await message.answer("Your search history is empty")


@router.message(StateFilter(None), Command(Commands.CANCEL))
async def cancel_command_no_qctive_query(message: Message):
    await message.answer("Active search dialog is not found")


@router.message(Command(Commands.CANCEL))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Search dialog is canceled")


@router.message(Command(Commands.START))
async def start_command(message: Message):
    if message.from_user:
        tg_user = message.from_user
        db.User.get_or_create(
            user_id=tg_user.id,
            first_name=tg_user.first_name,
        )

        await message.answer(
            Text(
                "Welcome, ",
                TextLink(tg_user.first_name, url=tg_user.url),
                "\nThis bot helps to search products on ",
                Bold("Amazon"),
                ".\nChoose a search command in the menu, or run ",
                f"{Commands.PREFIX}{Commands.HELP} ",
                "to get all bot's commands description",
            ).as_html(),
            parse_mode=ParseMode.HTML,
        )


@router.message(Command(Commands.HELP))
async def help_command(message: Message):
    descriptions = (
        Text(Bold("Bot can run the following commands:")),
        Text(
            f"{Commands.PREFIX}{Commands.LOW}",
            " - searches the prouct with the lowest price\n",
            "Required params:\n",
            Italic("product to search"),
            ", ",
            Italic("search results display limit"),
        ),
        Text(
            f"{Commands.PREFIX}{Commands.HIGH}",
            " - searches the prouct with the highest price\n",
            "Required params:\n",
            Italic("product to search"),
            ", ",
            Italic("search results display limit"),
        ),
        Text(
            f"{Commands.PREFIX}{Commands.CUSTOM}",
            " - searches the product within specified prices range\n",
            "Required params:\n",
            Italic("product to search"),
            ", ",
            Italic("minimum price"),
            ", ",
            Italic("maximum price"),
            ", ",
            Italic("search results display limit"),
        ),
        Text(
            f"For {Commands.PREFIX}{Commands.LOW}, ",
            f"{Commands.PREFIX}{Commands.HIGH} ",
            f"и {Commands.PREFIX}{Commands.CUSTOM} commands, ",
            "instead of using usual dialog, ",
            "you can also inline all the params with the command like this:\n",
            "/custom product min_price max_price limit",
        ),
        Text(f"{Commands.PREFIX}{Commands.CANCEL} - cancels current search dialog"),
        Text(
            f"{Commands.PREFIX}{Commands.HISTORY}",
            " - shows your last 5 search requests with the parameters inlined",
        ),
        Text(f"{Commands.PREFIX}{Commands.HELP} - shows bot's commands description"),
    )

    await message.answer(
        "\n\n".join(desc.as_html() for desc in descriptions),
        parse_mode=ParseMode.HTML,
    )
