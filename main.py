from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handles.message import router,init_db


load_dotenv()
Token=getenv("bot_token")

dp=Dispatcher()
dp.include_router(router)

async def main():
  bot=Bot(token=Token)
  
  await init_db()
  print("База данных готова.бот запущен!")


  await dp.start_polling(bot)



if __name__=="__main__":
  asyncio.run(main())   