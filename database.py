

import asyncio
import asyncpg
from config import get_db_url

async def init_db():
    conn = await asyncpg.connect(get_db_url())

    try:
        # Выполнение SQL-запроса для создания таблицы users
        await conn.execute('''
            CREATE TABLE Cursants(
                        id serial PRIMARY KEY,
                        Name char,
                        CurrentStatus bool
                    )
        ''')
        print("Таблица 'users' успешно создана.")
    finally:
        # Закрытие соединения
        await conn.close()

# Запуск асинхронной функции main
asyncio.run(init_db())
