import os
import dotenv
dotenv.load_dotenv()
import asyncio

from FloriaTelegramBotAPI import Bot

from . import route1


bot = Bot(os.environ['token'])
bot.Mount(route1.router)

asyncio.run(bot.Polling())
