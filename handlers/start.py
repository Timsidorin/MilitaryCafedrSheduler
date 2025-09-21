from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from create_bot import bot, scheduler
from Sheduler import Sheduler
from config import  CronScheduleSettings as cr
from config import configs
import logging

from keyboards.admin_keyboard import admin_keyboard

start_router = Router()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




@start_router.message(CommandStart())
async def cmd_start(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    scheduler.add_job(scheduled_message, 'cron',  day_of_week=cr.day_of_week, hour = cr.hour, minute = cr.minute, args=[chat_id])
    if str(user_id) in configs.ADMINS:
        await message.answer(
            'Привет! Я буду автоматически отправлять расписание дежурств и нарядов 221 уч.взвода.\n\n'
            '🔧 <b>Панель администратора доступна:</b>',
            reply_markup=admin_keyboard,
            parse_mode='HTML'
        )

    else:
        await message.answer(
            'Привет! Я буду автоматически отправлять расписание дежурств и нарядов 221 уч.взвода.', parse_mode='HTML')





async def send_message(chat_id: int, text: str):
    try:

        await bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")


async def scheduled_message(chat_id: int):
    query_scheduler = Sheduler("public.cursants")
    try:
        await query_scheduler.initialize()
        cursant =await query_scheduler.can_choice()
        cursant_name = f"<b>{cursant['name']}</b>"
        cursant_tg = cursant['telegram_name']
    finally:
        await query_scheduler.close()

    await send_message(chat_id, f"Дежурный на завтра курсант: {cursant_name} @{cursant_tg}")
