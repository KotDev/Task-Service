from pydantic import BaseModel


class CreateClientSchema(BaseModel):
    tg_id: int
    user_name: str
    admin: bool | None
    password: str


class JWTResponse(BaseModel):
    refresh_token: str
    access_token: str


class LoginClientSchema(BaseModel):
    tg_id: int
    password: str


class DetailClientSchema(BaseModel):
    tg_id: int
    user_name: str


class SuccessfulResponseSchema(BaseModel):
    result: bool


class ErrorSchema(BaseModel):
    error_type: str
    error_message: str