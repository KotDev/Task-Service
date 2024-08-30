from .db import AbstractManager, DB
from .models import Client, Base
from sqlalchemy import select


class BaseManager(DB):
    def __init__(self, base: Base) -> None:
        super().__init__()
        self.base = base

    async def clear_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)
            await conn.run_sync(self.base.metadata.create_all)

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)


class ClientManager(DB, AbstractManager):
    def __init__(self) -> None:
        super().__init__()

    async def create(self, obj: Client) -> None:
        async with self.async_session() as session:
            session.add(obj)
            await session.commit()

    async def get(self, params: dict) -> Client | None:
        async with self.async_session() as session:
            client = await session.execute(select(Client).where(Client.tg_id == params.get("tg_id")))
            return client.scalar_one_or_none()

    async def delete(self, params):
        pass

    async def update(self, new_values, params):
        pass
