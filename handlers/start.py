from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from create_bot import bot, scheduler
from Sheduler import Scheduler
from config import  CronScheduleDutySettings, CronScheduleDutySettings
from config import configs
import logging

from keyboards.admin_keyboard import admin_keyboard

start_router = Router()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




@start_router.message(CommandStart())
async def cmd_start(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    scheduler.add_job(scheduled_message_duty, 'cron',  day_of_week=CronScheduleDutySettings.day_of_week, hour = CronScheduleDutySettings.hour, minute = CronScheduleDutySettings.minute, args=[chat_id]) # Дежурство
    scheduler.add_job(scheduled_message_naryad, 'cron',  day_of_week=CronScheduleDutySettings.day_of_week, hour = CronScheduleDutySettings.hour, minute = CronScheduleDutySettings.minute, args=[chat_id]) # наряд

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


async def scheduled_message_duty(chat_id: int):
    query_scheduler = Scheduler("public.cursants")
    try:
        await query_scheduler.initialize()
        cursant =await query_scheduler.can_choice_duty()
        cursant_name = f"<b>{cursant['name']}</b>"
        cursant_tg = cursant['telegram_name']
    finally:
        await query_scheduler.close()

    await send_message(chat_id, f"Дежурный на завтра курсант: {cursant_name} @{cursant_tg}")



async def scheduled_message_naryad(chat_id: int):
    query_scheduler = Scheduler("public.cursants")
    try:
        await query_scheduler.initialize()
        cursants = await query_scheduler.can_choice_naryad()
        cursants_name = f"<b>{cursants['name']}</b>"
        cursants_tg = cursants['telegram_name']
    finally:
        await query_scheduler.close()
    await send_message(chat_id, f"В наряд идут: {cursants_name} @{cursants_tg}")











