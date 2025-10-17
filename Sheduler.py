import asyncio
import asyncpg
from typing import Optional
from config import get_db_url


class Scheduler:
    """
    Класс для управления планированием и выбором курсантов из базы данных.
    Обеспечивает последовательный выбор курсантов по ID с гарантированным порядком.
    """

    def __init__(self, table_name: str = "cursants"):
        self.table_name = table_name
        self.pool: Optional[asyncpg.Pool] = None
        self.max_id: int = 0

    async def initialize(self) -> None:
        """Инициализация пула соединений и получение максимального ID"""
        if not self.pool or self.pool.is_closed():
            db_url = get_db_url()
            self.pool = await asyncpg.create_pool(
                db_url,
                min_size=1,
                max_size=10,
                command_timeout=60,
                server_settings={
                    'application_name': 'military_scheduler',
                }
            )

            # Получаем максимальный ID для правильной логики сброса
            async with self.pool.acquire() as connection:
                query = f'SELECT COALESCE(MAX(id), 0) FROM {self.table_name}'
                self.max_id = await connection.fetchval(query)

    async def can_choice_duty(self) -> Optional[dict]:
        """
        Выбирает следующего курсанта по порядку ID.
        Возвращает информацию о выбранном курсанте или None.
        """
        if not self.pool:
            await self.initialize()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                # Выбираем следующего курсанта с минимальным ID и статусом '0'
                update_query = f"""
                    UPDATE {self.table_name}
                    SET currentstatus = '1'
                    WHERE id = (
                        SELECT id FROM {self.table_name}
                        WHERE currentstatus = '0'
                        ORDER BY id ASC
                        LIMIT 1
                        FOR UPDATE SKIP LOCKED
                    )
                    RETURNING id, name, telegram_name;
                """
                record = await connection.fetchrow(update_query)

                if not record:
                    return None

                # Если выбрали последнего курсанта, сбрасываем все статусы
                if record['id'] == self.max_id:
                    reset_query = f"UPDATE {self.table_name} SET currentstatus = '0'"
                    await connection.execute(reset_query)

                return {
                    'id': record['id'],
                    'name': record['name'],
                    'telegram_name': record['telegram_name']
                }

    async def can_choice_naryad(self) -> Optional[list]:
        """
        Выбирает курсантов для наряда
        """
        if not self.pool:
            await self.initialize()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                # Выбираем 3 курсантов с минимальными ID и статусом '0'
                update_query = f"""
                    UPDATE {self.table_name}
                    SET currentstatus = '1'
                    WHERE id IN (
                        SELECT id FROM {self.table_name}
                        WHERE currentstatus = '0'
                        ORDER BY id ASC
                        LIMIT 3
                        FOR UPDATE SKIP LOCKED
                    )
                    RETURNING id, name, telegram_name;
                """
                records = await connection.fetch(update_query)

                if not records:
                    return None

                # Проверяем, есть ли среди выбранных последний курсант
                selected_ids = [record['id'] for record in records]
                if self.max_id in selected_ids:
                    reset_query = f"UPDATE {self.table_name} SET currentstatus = '0'"
                    await connection.execute(reset_query)

                return [
                    {
                        'id': record['id'],
                        'name': record['name'],
                        'telegram_name': record['telegram_name']
                    }
                    for record in records
                ]

    async def get_all_cursants(self) -> list:
        """Получить всех курсантов в правильном порядке по ID"""
        if not self.pool:
            await self.initialize()

        async with self.pool.acquire() as connection:
            query = f"SELECT * FROM {self.table_name} ORDER BY id ASC"
            records = await connection.fetch(query)
            return [dict(record) for record in records]

    async def reset_all_status(self) -> None:
        """Сбросить статус всех курсантов в '0'"""
        if not self.pool:
            await self.initialize()

        async with self.pool.acquire() as connection:
            query = f"UPDATE {self.table_name} SET currentstatus = '0'"
            await connection.execute(query)

    async def get_current_cursant(self) -> Optional[dict]:
        """Получить текущего активного курсанта (со статусом '1')"""
        if not self.pool:
            await self.initialize()

        async with self.pool.acquire() as connection:
            query = f"""
                SELECT id, name, telegram_name 
                FROM {self.table_name} 
                WHERE currentstatus = '1' 
                ORDER BY id ASC 
                LIMIT 1
            """
            record = await connection.fetchrow(query)
            return dict(record) if record else None

    async def close(self) -> None:
        """Закрытие пула соединений"""
        if self.pool and not self.pool.close():
            await self.pool.close()


# Глобальный экземпляр планировщика
_global_scheduler: Optional[Scheduler] = None


async def get_scheduler() -> Scheduler:
    """Получить глобальный экземпляр планировщика (Singleton pattern)"""
    global _global_scheduler
    if _global_scheduler is None:
        _global_scheduler = Scheduler()
        await _global_scheduler.initialize()
    return _global_scheduler


async def scheduled_message(chat_id: int):
    """
    Функция для выполнения запланированных сообщений.
    Использует глобальный экземпляр планировщика.
    """
    try:
        scheduler = await get_scheduler()
        cursant = await scheduler.can_choice()

        if cursant:
            print(f"Выбран курсант: {cursant['name']} (ID: {cursant['id']}, TG: {cursant['telegram_name']})")
            # Здесь добавьте логику отправки сообщения
            # await bot.send_message(chat_id, f"Очередь: {cursant['name']}")
        else:
            print("Нет доступных курсантов")

    except Exception as e:
        print(f"Ошибка в scheduled_message: {e}")


async def main():
    """Пример использования"""
    scheduler = Scheduler()
    try:
        await scheduler.initialize()

        print("=== Все курсанты ===")
        all_cursants = await scheduler.get_all_cursants()
        for cursant in all_cursants:
            print(
                f"ID: {cursant['id']:2d}, Name: {cursant['name']:<12}, Status: {cursant['currentstatus']}, TG: {cursant['telegram_name']}")

        print("\n=== Выбираем 5 курсантов ===")
        for i in range(5):
            result = await scheduler.can_choice()
            if result:
                print(f"{i + 1}. {result['name']} (ID: {result['id']})")
            else:
                print(f"{i + 1}. Нет доступных курсантов")

        print("\n=== Текущий активный курсант ===")
        current = await scheduler.get_current_cursant()
        if current:
            print(f"Активный: {current['name']} (ID: {current['id']})")

        # Сброс статусов
        await scheduler.reset_all_status()
        print("\n=== Статусы сброшены ===")

    finally:
        await scheduler.close()


if __name__ == "__main__":
    asyncio.run(main())
