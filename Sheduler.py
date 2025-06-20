import asyncio
import asyncpg
from config import get_db_url


class Sheduler():
    def __init__(self, table_name):
        self.table_name = table_name
        self.pool = None

    async def initialize(self):
        if not self.pool:
            db_url = get_db_url()
            self.pool = await asyncpg.create_pool(db_url)
            async with self.pool.acquire() as connection:
                query = f'SELECT COUNT(*) FROM {self.table_name}'
                self.count = await connection.fetchval(query)

    async def can_choice(self) ->str:
        async with self.pool.acquire() as connection:
            query = f"""
                UPDATE {self.table_name}
                SET currentstatus = '1'
                WHERE id = (
                    SELECT id FROM {self.table_name}
                    WHERE currentstatus = '0'
                    ORDER BY id
                    LIMIT 1
                    FOR UPDATE SKIP LOCKED
                )
                RETURNING id, name, telegram_name;
            """
            record = await connection.fetchrow(query)
            if record['id'] == self.count:
                query = f"UPDATE {self.table_name} SET currentstatus = '0'"
                await connection.fetchrow(query)
            if record:
                return record

    async def close(self):
        if self.pool:
            await self.pool.close()

async def main():
    query_scheduler = Sheduler("public.cursants")
    try:
        await query_scheduler.initialize()
        await query_scheduler.can_choice()
    finally:
        await query_scheduler.close()


if __name__ == "__main__":
    asyncio.run(main())

