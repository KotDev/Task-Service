from database.schemas import (CreateClientSchema,
                                           LoginClientSchema,
                                           JWTResponse,
                                           ErrorSchema,
                                           SuccessfulResponseSchema,
                                           )
from database.manager import ClientManager
from database.models import Client
from werkzeug.security import check_password_hash, generate_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException


class AuthLogicManager(ClientManager):
    def __init__(self) -> None:
        super().__init__()

    async def register_user(self, schema: CreateClientSchema):
        schema.password = generate_password_hash(schema.password)
        obj = Client(**schema.dict())
        await self.create(obj=obj)
        response_schema: SuccessfulResponseSchema = SuccessfulResponseSchema(result=True)
        return response_schema

    async def login_user(self, schema: LoginClientSchema, auth: AuthJWT) -> JWTResponse:
        client: Client | None = await self.get(params={"tg_id": schema.tg_id})
        if client is None:
            detail_error = ErrorSchema(error_type="AuthError", error_message="Пользователь не зарегестрирован")
            raise HTTPException(status_code=404, detail=detail_error.dict())
        elif not check_password_hash(client.password, schema.password):
            detail_error = ErrorSchema(error_type="AuthError", error_message="Не верный пороль или tg id")
            raise HTTPException(status_code=403, detail=detail_error.dict())
        access_token = auth.create_access_token(subject=client.tg_id, fresh=True, user_claims={"admin": client.admin})
        refresh_token = auth.create_refresh_token(subject=client.tg_id, user_claims={"admin": client.admin})
        return JWTResponse(access_token=access_token, refresh_token=refresh_token)

    async def create_new_access_refresh_token(self, auth: AuthJWT) -> JWTResponse:
        current_user = auth.get_jwt_subject()
        role_user = auth.get_raw_jwt()["admin"]
        new_refresh_token = auth.create_refresh_token(subject=current_user)
        new_access_token = auth.create_access_token(subject=current_user, fresh=False, user_claims={"admin": role_user})
        return JWTResponse(refresh_token=new_refresh_token, access_token=new_access_token)


def get_auth_logic_manager() -> AuthLogicManager:
    return AuthLogicManager()

