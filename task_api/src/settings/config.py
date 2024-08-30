from pathlib import Path

from pydantic_settings import BaseSettings
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent


class SettingsDB(BaseModel):
    db_url: str = "postgresql+asyncpg://root:root@localhost:5433/task_db"
    echo: bool = True
    expire_on_commit: bool = False
    autocommit: bool = False
    autoflush: bool = False


class SettingsJWT(BaseModel):
    authjwt_private_key: str = str((BASE_DIR / "certs" / "jwt-private.pem").read_text())
    authjwt_public_key: str = str((BASE_DIR / "certs" / "jwt-public.pem").read_text())
    authjwt_algorithm: str = "RS512"


class Settings(BaseSettings):
    db_settings: SettingsDB = SettingsDB()
    jwt_settings: SettingsJWT = SettingsJWT()


@AuthJWT.load_config
def get_jwt_settings():
    return SettingsJWT()


settings = Settings()