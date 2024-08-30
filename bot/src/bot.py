import asyncio

from aiogram import Bot
from bot.src.settings.config import settings
from bot.src.settings.dispatcher import dp


bot = Bot(token=settings.bot_settings.token)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())