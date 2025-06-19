



from create_bot import bot
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



async def send_message(chat_id: int, text: str):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

# Функция, которая будет запускаться по расписанию
async def scheduled_message(chat_id: int):
    await send_message(chat_id, "Это сообщение отправлено по расписанию!")