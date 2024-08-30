from pydantic import BaseModel, root_validator, validator, model_validator
from datetime import datetime

from typing_extensions import List


class DateTime(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int

    @validator("*", pre=True)
    def validate_datetime(cls, value):
        try:
            datetime(value['year'], value['month'], value['day'], value['hour'], value['minute'])
        except ValueError:
            raise ValueError("Некорректные данные даты и времени")
        return value


class CreateTaskRequestSchema(BaseModel):
    title: str
    description: str
    datetime: DateTime

    @validator("title")
    def validate_title(cls, value: str):
        if len(value) > 70:
            raise ValueError("Превышена длинна допустимого названия задачи")
        return value


class DetailTaskResponseSchema(BaseModel):
    title: str
    description: str
    status_task: str
    scheduled_datetime: str


class TaskFeedElementSchema(BaseModel):
    id: int
    title: str


class TaskFeedResponseSchema(BaseModel):
    tasks: List["TaskFeedElementSchema"]


class ErrorResponseSchema(BaseModel):
    error_type: str
    error_message: str


class SuccessfulResponseSchema(BaseModel):
    result: bool
