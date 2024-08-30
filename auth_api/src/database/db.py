from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings.config import settings
from abc import ABC, abstractmethod


class DB:
    def __init__(self) -> None:
        self.settings_db = settings.db_settings
        self.engine = create_async_engine(url=self.settings_db.db_url, echo=self.settings_db.echo)
        self.async_session = async_sessionmaker(self.engine,
                                                autoflush=self.settings_db.autoflush,
                                                autocommit=self.settings_db.autocommit,
                                                expire_on_commit=self.settings_db.expire_on_commit,
                                                class_=AsyncSession,
                                                )


class AbstractManager(ABC):
    @abstractmethod
    def create(self, obj):
        pass

    @abstractmethod
    def delete(self, params):
        pass

    @abstractmethod
    def update(self, new_values, params):
        pass

    @abstractmethod
    def get(self, params):
        pass