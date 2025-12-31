import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher

from database.models import async_main
from handlers.user import user # Импортируем роутер
from handlers.targets import target
from handlers.roadmaps import roadmap

async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user, target, roadmap) # Подключаем роутер
    dp.startup.register(startup)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await async_main()

if __name__  == '__main__':
    print('Бот включен!')
    try:
        asyncio.run(main())  
    except KeyboardInterrupt:
        print('Бот выключен!')