from pydantic_settings import BaseSettings
from pydantic import BaseModel
from aiogram.fsm.storage.memory import MemoryStorage
from .api_config import APIModel


class BotSettings(BaseModel):
    token: str = " "
    storage: MemoryStorage = MemoryStorage()


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    expire_refresh_token: int = 2_592_000


class Settings(BaseSettings):
    bot_settings: BotSettings = BotSettings()
    redis_settings: RedisSettings = RedisSettings()
    api_model: APIModel = APIModel()


settings = Settings()


