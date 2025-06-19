from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from create_bot import bot, scheduler
from Sheduler import Sheduler
from config import  CronScheduleSettings as cr
import logging

start_router = Router()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




@start_router.message(CommandStart())
async def cmd_start(message: Message):
    chat_id = message.chat.id
    scheduler.add_job(scheduled_message, 'cron',  day_of_week=cr.day_of_week, hour = cr.hour, minute = cr.minute, args=[chat_id])
    await message.answer('Привет! Я буду автоматически отправлять расписание дежурств и нарядов 221 уч.взвода')




async def send_message(chat_id: int, text: str):
    try:

        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


async def scheduled_message(chat_id: int):
    query_scheduler = Sheduler("public.cursants")
    try:
        await query_scheduler.initialize()
        cursant = await query_scheduler.can_choice()
        cursant_name_formatted = f"<b>{cursant['name']}</b>"
    finally:
        await query_scheduler.close()

    await send_message(chat_id, f"Дежурный на завтра курсант: {cursant_name_formatted}")
