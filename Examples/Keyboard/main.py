import os
import dotenv
dotenv.load_dotenv()
import asyncio

from FloriaTelegramBotAPI import Bot
from FloriaTelegramBotAPI.Types.EasyTypes import *
from FloriaTelegramBotAPI.Filters import *
from FloriaTelegramBotAPI.Enums import ChatType
from FloriaTelegramBotAPI.Types.EasyTypes.Keyboards.Keyboard import *


bot = Bot(os.environ['token'])

@bot.Message()
async def _(message: Message):
    await message.Answer(
        message.text,
        reply_markup=Keyboard(
            Button('Обычная кнопка'), Button('Поделиться контактом', request_contact=True), ENDL,
            Button('Еще одна кнопка'),
            
            resize=True
        ).As_Markup()
    )

asyncio.run(bot.Polling())
