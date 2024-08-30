from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from database.schemas import DetailClientSchema
from logic.client_logic import ClientLogicManager, get_client_logic_manager

router = APIRouter(prefix="/client", tags=["Client"])


@router.get("/me")
async def get_me_info_point(manager: ClientLogicManager = Depends(get_client_logic_manager),
                            Authorize: AuthJWT = Depends(),
                            ) -> DetailClientSchema:
    Authorize.fresh_jwt_required()
    tg_id: int = Authorize.get_jwt_subject()
    response: DetailClientSchema = await manager.get_user(tg_id=tg_id)
    return response
