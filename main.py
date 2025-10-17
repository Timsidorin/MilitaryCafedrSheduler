import asyncio
import sys
from tendo import singleton
from create_bot import bot, dp, scheduler
from handlers.start import start_router


async def main():
    # Автоматически предотвращает повторный запуск
    me = singleton.SingleInstance()  # sys.exit(-1) если уже запущен
    dp.include_router(start_router)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




