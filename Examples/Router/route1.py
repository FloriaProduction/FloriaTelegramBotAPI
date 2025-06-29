from FloriaTelegramBotAPI import Router
from FloriaTelegramBotAPI.Types.EasyTypes import *
from FloriaTelegramBotAPI.Handlers.Filters import *
from FloriaTelegramBotAPI.Enums import ChatType


router = Router()


@router.Message(Command('start'), Chat(ChatType.PRIVATE))
async def _(message: Message):
    await message.Answer('Hello!')

@router.Message()
async def _(message: Message):
    await message.Answer(message.text)
