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
            await message.answer("Ваши последние запросы:")
            for entry in history:
                await message.answer(entry.query)
        else:
            await message.answer("Ваша история запросов пуста")


@router.message(StateFilter(None), Command(Commands.CANCEL))
async def cancel_command_no_qctive_query(message: Message):
    await message.answer("Активный запрос не найден")


@router.message(Command(Commands.CANCEL))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Запрос отменён")


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
                "Добро пожаловать, ",
                TextLink(tg_user.first_name, url=tg_user.url),
                "\nЭтот бот поможет вам найти товары на площадке ",
                Bold("Amazon"),
                ".\nВыберите режим запроса в меню, или введите ",
                f"{Commands.PREFIX}{Commands.HELP} ",
                "для получения описания всех команд бота",
            ).as_html(),
            parse_mode=ParseMode.HTML,
        )


@router.message(Command(Commands.HELP))
async def help_command(message: Message):
    descriptions = (
        Text(Bold("Бот может выполнять следующие команды:")),
        Text(
            f"{Commands.PREFIX}{Commands.LOW}",
            " - поиск товара по наиболее низкой цене\n",
            "Запрашиваемые параметры:\n",
            Italic("товар для поиска"),
            ", ",
            Italic("кол-во отображаемых результатов"),
        ),
        Text(
            f"{Commands.PREFIX}{Commands.HIGH}",
            " - поиск товара по наиболее высокой цене\n",
            "Запрашиваемые параметры:\n",
            Italic("товар для поиска"),
            ", ",
            Italic("кол-во отображаемых результатов"),
        ),
        Text(
            f"{Commands.PREFIX}{Commands.CUSTOM}",
            " - поиск товара с указанием ценового диапазона поиска\n",
            "Запрашиваемые параметры:\n",
            Italic("товар для поиска"),
            ", ",
            Italic("минимальная цена"),
            ", ",
            Italic("максимальная цена"),
            ", ",
            Italic("кол-во отображаемых результатов"),
        ),
        Text(
            "Для команд ",
            f"{Commands.PREFIX}{Commands.LOW}, ",
            f"{Commands.PREFIX}{Commands.HIGH} ",
            f"и {Commands.PREFIX}{Commands.CUSTOM}, ",
            "помимо стандартного диалога запроса, ",
            "доступен формат однострочного запроса ",
            "с указанием параметров через пробел. Пример:\n",
            "/custom товар мин_цена макс_цена лимит",
        ),
        Text(f"{Commands.PREFIX}{Commands.CANCEL} - отменяет текущий диалог запроса"),
        Text(
            f"{Commands.PREFIX}{Commands.HISTORY}",
            " - выводит ваши последние 5 запросов с указанными параметрами",
        ),
        Text(f"{Commands.PREFIX}{Commands.HELP} - описание всех команд бота"),
    )

    await message.answer(
        "\n\n".join(desc.as_html() for desc in descriptions),
        parse_mode=ParseMode.HTML,
    )
