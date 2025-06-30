import os
import dotenv
dotenv.load_dotenv()
import asyncio

from FloriaTelegramBotAPI import Bot, Router

from . import food


bot = Bot(os.environ['token'])

bot.Mount(food.fsm)

asyncio.run(bot.Polling())