from fastapi import APIRouter
from controllers.auth_controller import router as auth_router
from controllers.client_controller import router as client_router

main_router = APIRouter(prefix="/auth_api", tags=["Main"])

main_router.include_router(auth_router)
main_router.include_router(client_router)