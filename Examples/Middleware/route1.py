from FloriaTelegramBotAPI import Router
from FloriaTelegramBotAPI.Middleware import Middleware
from FloriaTelegramBotAPI.Types.EasyTypes import *
from FloriaTelegramBotAPI.Filters import *
from FloriaTelegramBotAPI.Enums import ChatType


class LogMiddleware(Middleware):
    async def Invoke(self, handler, obj, bot, **kwargs):
        print(f'Before')
        result = await super().Invoke(handler, obj, bot, **kwargs)
        print(f'After')
        
        return result


router = Router()
router.middleware = LogMiddleware()


@router.Message(Command('start'), Chat(ChatType.PRIVATE))
async def _(message: Message):
    await message.Answer('Hello!')

@router.Message()
async def _(message: Message):
    await message.Answer(message.text)

