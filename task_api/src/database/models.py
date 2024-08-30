from sqlalchemy.orm import (declarative_base,
                            Mapped,
                            mapped_column,
                            )
from sqlalchemy import Text, DateTime, String
from typing_extensions import Annotated

obj_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

Base = declarative_base()


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[obj_id]
    title: Mapped[str] = mapped_column(String(70), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status_task: Mapped[str] = mapped_column(String(15), default="not done")
    client_id: Mapped[int] = mapped_column(nullable=False)
    scheduled_datetime: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
