from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Я буду автоматически отправлять расписание дежурств и нарядов 221 уч.взвода')


