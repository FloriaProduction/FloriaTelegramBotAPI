import os
import dotenv
dotenv.load_dotenv()
import asyncio

from FloriaTelegramBotAPI import Bot
from FloriaTelegramBotAPI.Types.EasyTypes import *
from FloriaTelegramBotAPI.Filters import *
from FloriaTelegramBotAPI.Enums import ChatType


bot = Bot(os.environ['token'])

@bot.Message(Command('start'), Chat(ChatType.PRIVATE))
async def _(message: Message):
    await message.Answer('Hello!')

@bot.Message()
async def _(message: Message):
    await message.Answer(message.text)

asyncio.run(bot.Polling())
