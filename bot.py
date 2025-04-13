import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher
from utils.config import settings
from database.models import engine, Base
from handlers.main_handler import main_router
from handlers.admin_handler import admin_router

bot = Bot(token=settings.TOKEN)

dp = Dispatcher()

# dp.include_router(admin_router)
dp.include_router(main_router)


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("By by, homie")


# async def async_main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(async_main())