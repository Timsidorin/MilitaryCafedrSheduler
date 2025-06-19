import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from handlers.start import scheduled_message

async def main():
    dp.include_router(start_router)
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())