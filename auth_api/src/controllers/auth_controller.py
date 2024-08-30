from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from database.schemas import CreateClientSchema, LoginClientSchema, SuccessfulResponseSchema, JWTResponse
from logic.auth_logic import AuthLogicManager, get_auth_logic_manager

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user_point(schema: CreateClientSchema,
                              manager: AuthLogicManager = Depends(get_auth_logic_manager)) -> SuccessfulResponseSchema:
    response: SuccessfulResponseSchema = await manager.register_user(schema)
    return response


@router.post("/login")
async def login_user_point(schema: LoginClientSchema,
                           manager: AuthLogicManager = Depends(get_auth_logic_manager),
                           Authorize: AuthJWT = Depends(),
                           ) -> JWTResponse:
    response: JWTResponse = await manager.login_user(schema, Authorize)
    return response


@router.put("/refresh")
async def update_jwt_token_point(manager: AuthLogicManager = Depends(get_auth_logic_manager),
                                 Authorize: AuthJWT = Depends()
                                 ) -> JWTResponse:
    Authorize.jwt_refresh_token_required()
    response: JWTResponse = await manager.create_new_access_refresh_token(auth=Authorize)
    return response
