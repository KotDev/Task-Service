from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
#from auth_dialog.states import
from aiohttp import ClientSession
from redis.asyncio import Redis
from bot.src.settings.config import settings
from bot.src.settings.api_config import request

redis_client = Redis(host=settings.redis_settings.host,
                     port=settings.redis_settings.port,
                     db=0)
router = Router()
router.include_routers(
    ...
)


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    api_model = settings.api_model
    tokens = await redis_client.lrange(str(message.from_user.id), 0, -1)
    if not tokens:
        await dialog_manager.start(mode=StartMode.RESET_STACK)
    else:
        tokens_decoded = [token.decode('utf-8') for token in tokens]
        access_token = tokens_decoded[0]
        refresh_token = tokens_decoded[1]
        async with ClientSession as session:
            response = await request(session=session,
                                     url=api_model.client_api_urls.me,
                                     headers={"Authorization": f"Bearer {access_token}",
                                               "Refresh-Authorization": f"Bearer {refresh_token}"},
                                     method="get")
            if response.status_code == 401:
                response = await request(session=session,
                                         url=api_model.auth_api_urls.refresh,
                                         headers={"Authorization":
                                                      f"Bearer {access_token}",
                                                  "Refresh-Authorization":
                                                      f"Bearer {refresh_token}"},
                                         method="put")
                if response.status_code == 200:
                    await redis_client.lset(str(message.from_user.id), 0, response.json_data["access_token"])
                    await redis_client.lset(str(message.from_user.id), 1, response.json_data["refresh_token"])
                    await redis_client.expire(str(message.from_user.id), settings.redis_settings.expire_refresh_token)
                    await dialog_manager.start(mode=StartMode.RESET_STACK)
                else:
                    await dialog_manager.start(mode=StartMode.RESET_STACK)
            else:
                await dialog_manager.start(mode=StartMode.RESET_STACK)

