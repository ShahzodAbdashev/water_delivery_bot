import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher
from utils.config import settings

bot = Bot(token=settings.TOKEN)

dp = Dispatcher()


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("By by, homie")