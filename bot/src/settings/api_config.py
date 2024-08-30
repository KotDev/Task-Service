from dataclasses import dataclass

from aiohttp import ClientSession
from pydantic import BaseModel


@dataclass
class ResponseData:
    json_data: dict
    status_code: int


class AuthAPI(BaseModel):
    port: str = "8000"
    host: str = "0.0.0.0"
    register: str = f"{host}:{port}/auth_api/auth/register"
    login: str = f"{host}:{port}/auth_api/auth/login"
    refresh: str = f"{host}:{port}/auth_api/auth/refresh"


class ClientAPI(BaseModel):
    port: str = "8000"
    host: str = "0.0.0.0"
    me: str = f"{host}:{port}/auth_api/client/me"


class TaskAPI(BaseModel):
    port: str = "8001"
    host: str = "0.0.0.0"
    create: str = f"{host}:{port}/task_api/tasks/create"
    feeds: str = f"{host}:{port}/task_api/tasks/feeds/"
    info: str = f"{host}:{port}/task_api/tasks/info/"
    status: str = f"{host}:{port}/task_api/tasks/status/"
    delete: str = f"{host}:{port}/task_api/tasks/delete/"


class APIModel(BaseModel):
    auth_api_urls: AuthAPI = AuthAPI()
    client_api_urls: ClientAPI = ClientAPI()
    task_api_urls: TaskAPI = TaskAPI()


async def request(
    session: ClientSession,
    url: str,
    method: str,
    json_data: dict | None = None,
    headers: dict | None = None,
    params: dict | None = None
) -> ResponseData:
    async with getattr(session, method)(url, json=json_data, headers=headers, params=params) as response:
        data = await response.json()
        return ResponseData(json_data=data, status_code=response.status)
