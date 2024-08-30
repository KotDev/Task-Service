from aiogram import Dispatcher
from .config import settings
from aiogram_dialog import setup_dialogs

dp = Dispatcher(storage=settings.bot_settings.storage)
dp.include_router()
setup_dialogs(dp)
