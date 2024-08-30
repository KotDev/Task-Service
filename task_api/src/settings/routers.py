from fastapi import APIRouter
from controllers.task_controller import router as task_router

main_router = APIRouter(prefix="/task_api", tags=["Main"])

main_router.include_router(task_router)
