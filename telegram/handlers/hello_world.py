from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("hello_world"))
async def hello_world(message: Message):
    await message.reply("Hello, world!")


@router.message(F.text == "Привет")
async def hello(message: Message):
    await message.reply("Привет!")
