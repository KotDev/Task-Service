from sqlalchemy.orm import (declarative_base,
                            Mapped,
                            mapped_column,
                            )
from sqlalchemy import Text, String
from typing_extensions import Annotated

obj_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"
    id: Mapped[obj_id]
    tg_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    user_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(Text())
    admin: Mapped[bool] = mapped_column(default=False)