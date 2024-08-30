from fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends

from database.schemas import (CreateTaskRequestSchema,
                              DetailTaskResponseSchema,
                              TaskFeedResponseSchema,
                              SuccessfulResponseSchema,
                              )

from logic.task_logic import get_logic_manager, TaskLogicManager


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create", response_model=SuccessfulResponseSchema)
async def create_new_task_point(schema: CreateTaskRequestSchema,
                                manager: TaskLogicManager = Depends(get_logic_manager),
                                Authorize: AuthJWT = Depends()) -> SuccessfulResponseSchema:
    Authorize.fresh_jwt_required()
    client_id: int = Authorize.get_jwt_subject()
    response: SuccessfulResponseSchema = await manager.create_new_task(schema, client_id)
    return response


@router.get("/feeds/", response_model=TaskFeedResponseSchema)
async def get_feed_tasks_point(today: bool,
                               status: str,
                               manager: TaskLogicManager = Depends(get_logic_manager),
                               Authorize: AuthJWT = Depends()) -> TaskFeedResponseSchema:
    Authorize.fresh_jwt_required()
    client_id: int = Authorize.get_jwt_subject()
    response: TaskFeedResponseSchema = await manager.get_tasks_feed(client_id=client_id,
                                                                    today=today,
                                                                    status=status)
    return response


@router.get("/info/{task_id}", response_model=DetailTaskResponseSchema)
async def get_task_info_point(task_id: int,
                              manager: TaskLogicManager = Depends(get_logic_manager),
                              Authorize: AuthJWT = Depends()) -> DetailTaskResponseSchema:
    Authorize.fresh_jwt_required()
    client_id: int = Authorize.get_jwt_subject()
    response: DetailTaskResponseSchema = await manager.get_task_info(task_id=task_id,
                                                                     client_id=client_id)
    return response


@router.put("/status/{task_id}/", response_model=SuccessfulResponseSchema)
async def update_status_task_point(task_id: int,
                                   status: str,
                                   manager: TaskLogicManager = Depends(get_logic_manager),
                                   Authorize: AuthJWT = Depends()) -> SuccessfulResponseSchema:
    Authorize.fresh_jwt_required()
    client_id: int = Authorize.get_jwt_subject()
    response: SuccessfulResponseSchema = await manager.update_task_status(client_id=client_id,
                                                                          task_id=task_id,
                                                                          status=status)
    return response


@router.delete("/delete/{task_id}", response_model=SuccessfulResponseSchema)
async def delete_task_point(task_id: int,
                            manager: TaskLogicManager = Depends(get_logic_manager),
                            Authorize: AuthJWT = Depends()) -> SuccessfulResponseSchema:
    Authorize.fresh_jwt_required()
    client_id: int = Authorize.get_jwt_subject()
    response: SuccessfulResponseSchema = await manager.delete_task(client_id=client_id,
                                                                   task_id=task_id)
    return response
