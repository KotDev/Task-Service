from datetime import datetime

from database.manager import TasksManager
from database.models import Tasks
from database.schemas import (CreateTaskRequestSchema,
                              DetailTaskResponseSchema,
                              TaskFeedElementSchema,
                              TaskFeedResponseSchema,
                              SuccessfulResponseSchema,
                              )


class TaskLogicManager(TasksManager):
    def __init__(self) -> None:
        super().__init__()

    async def get_task_info(self, task_id: int, client_id: int) -> DetailTaskResponseSchema:
        task_info: Tasks = await self.get(params={"task_id": task_id, "client_id": client_id})
        return DetailTaskResponseSchema(title=task_info.title,
                                        status_task=task_info.status_task,
                                        scheduled_datetime=task_info.scheduled_datetime,
                                        description=task_info.description,
                                        )

    async def get_tasks_feed(self, client_id: int, today: bool, status: str) -> TaskFeedResponseSchema:
        tasks_feed: list[Tasks] | [] = await self.get_feed(params={"client_id": client_id,
                                                                   "today": today,
                                                                   "status": status})
        return TaskFeedResponseSchema(tasks=[TaskFeedElementSchema(id=elem.id, title=elem.title)
                                             for elem in tasks_feed] if tasks_feed else [])

    async def create_new_task(self, schema: CreateTaskRequestSchema, client_id: int) -> SuccessfulResponseSchema:
        should_datetime = datetime(schema.year, schema.month, schema.day, schema.hour, schema.minute)
        obj = Tasks(title=schema.title,
                    description=schema.description,
                    client_id=client_id,
                    scheduled_datetime=should_datetime)
        await self.create(obj)
        return SuccessfulResponseSchema(result=True)

    async def update_task_status(self, client_id: int, task_id: int, status: str) -> SuccessfulResponseSchema:
        await self.update(new_values={"status_task": status},
                          params={"client_id": client_id, "task_id": task_id})
        return SuccessfulResponseSchema(result=True)

    async def delete_task(self, client_id: int, task_id: int) -> SuccessfulResponseSchema:
        await self.delete(params={"task_id": task_id, "client_id": client_id})
        return SuccessfulResponseSchema(result=True)


def get_logic_manager() -> TaskLogicManager:
    return TaskLogicManager()