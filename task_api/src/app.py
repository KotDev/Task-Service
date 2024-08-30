import uvicorn
from fastapi import FastAPI, Request, HTTPException

from database.manager import BaseManager
from database.models import Base
from settings.routers import main_router
from database.schemas import ErrorResponseSchema
from fastapi_jwt_auth.exceptions import AuthJWTException, FreshTokenRequired, JWTDecodeError
from aiohttp import ClientSession

app = FastAPI()

app.include_router(main_router)


@app.exception_handler(AuthJWTException)
async def auth_jwt_exception_handler(request: Request, exc: AuthJWTException):
    access_token = request.headers.get("Authorization")
    refresh_token = request.headers.get("Refresh-Authorization")
    if refresh_token or access_token is None:
        detail_error = ErrorResponseSchema(error_type="AuthError", error_message="Token is missing")
        raise HTTPException(status_code=401, detail=detail_error.dict())
    access_token.replace("Bearer ", "")
    refresh_token.replace("Bearer ", "")
    if isinstance(exc, FreshTokenRequired):
        async with ClientSession() as session:
            async with session.put("0.0.0.0:8000/auth_api/auth/refresh", headers={"Authorization": f"Bearer {access_token}",
                                                "Refresh-Authorization": f"Bearer {refresh_token}"}) as response:
                if response.status == 401:
                    detail_error = ErrorResponseSchema(error_type="AuthError", error_message="User is not auth")
                    raise HTTPException(status_code=403, detail=detail_error.dict())
                response_json = await response.json()
                return response_json
    if isinstance(exc, JWTDecodeError):
        detail_error = ErrorResponseSchema(error_type="AuthError", error_message="Token is not decoding")
        raise HTTPException(status_code=401, detail=detail_error.dict())


@app.on_event("startup")
async def start_app():
    base_manager = BaseManager(Base)
    await base_manager.init_models()
    await base_manager.clear_models()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)