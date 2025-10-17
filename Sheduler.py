import asyncpg
from typing import Optional
from config import get_db_url


class Scheduler:
    """Управление выбором курсантов из БД"""

    pool: Optional[asyncpg.Pool] = None
    max_id: int = 0
    table_name: str = "cursants"

    @classmethod
    async def init(cls):
        """Инициализация пула один раз"""
        if cls.pool is None:
            cls.pool = await asyncpg.create_pool(get_db_url(), min_size=2, max_size=10)
            cls.max_id = await cls.pool.fetchval(f'SELECT COALESCE(MAX(id), 0) FROM {cls.table_name}')

    @classmethod
    async def choice(cls, count: int = 1) -> Optional[list]:
        """
        Выбирает курсантов для дежурства/наряда
        count=1 для дежурного, count=3 для наряда
        """
        async with cls.pool.acquire() as conn:
            async with conn.transaction():
                records = await conn.fetch(f"""
                    UPDATE {cls.table_name} SET currentstatus = '1'
                    WHERE id IN (
                        SELECT id FROM {cls.table_name}
                        WHERE currentstatus = '0'
                        ORDER BY id ASC LIMIT {count}
                        FOR UPDATE SKIP LOCKED
                    )
                    RETURNING id, name, telegram_name
                """)

                if records and any(r['id'] == cls.max_id for r in records):
                    await conn.execute(f"UPDATE {cls.table_name} SET currentstatus = '0'")

                return [dict(r) for r in records] if records else None

    @classmethod
    async def reset_all(cls):
        """Сброс всех статусов"""
        await cls.pool.execute(f"UPDATE {cls.table_name} SET currentstatus = '0'")


# Пример использования
async def main():
    await Scheduler.init()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
