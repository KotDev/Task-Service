from .db import AbstractManager, DB
from .models import Tasks, Base
from sqlalchemy import select, delete, update, Date, func, cast, and_
from datetime import date


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


class TasksManager(DB, AbstractManager):
    def __init__(self) -> None:
        super().__init__()

    async def create(self, obj: Tasks) -> None:
        async with self.async_session() as session:
            session.add(obj)
            await session.commit()

    async def delete(self, params: dict) -> None:
        async with self.async_session() as session:
            await session.execute(delete(Tasks).filter(Tasks.id == params.get("task_id"),
                                                       Tasks.client_id == params.get("client_id")))

    async def get(self, params: dict) -> Tasks | None:
        async with self.async_session() as session:
            if params.get("task_id") is not None:
                task = await session.execute(select(Tasks).filter(Tasks.id == params.get("task_id"),
                                                                  Tasks.client_id == params.get("client_id")))
            else:
                task = await session.execute(select(Tasks).where(Tasks.scheduled_datetime == params.get("scheduled_datetime"),
                                                                 Tasks.client_id == params.get("client_id")))
            return task.scalar_one_or_none()

    async def update(self, new_values: dict, params: dict) -> None:
        async with self.async_session() as session:
            await session.execute(update(Tasks).filter(Tasks.id == params.get("task_id"),
                                                       Tasks.client_id == params.get("client_id")).values(**params))
            await session.commit()

    async def get_feed(self, params: dict) -> list[Tasks]:
        filters = []
        if params.get("today") is not None and params.get("today"):
            today = date.today()
            filters.append(cast(Tasks.scheduled_datetime, Date) == today)
        if params.get("status") is not None and params.get("status"):
            filters.append(Tasks.status_task == params.get("status"))
        async with self.async_session() as session:
            tasks_feed = await session.execute(
                select(Tasks.id, Tasks.title)
                .where(and_(
                    Tasks.client_id == params.get("client_id"),
                    *filters,
                ))
            )
            return tasks_feed.scalars().all()
