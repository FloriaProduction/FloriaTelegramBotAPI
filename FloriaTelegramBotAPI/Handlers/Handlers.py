from .BaseHandler import Handler
from ..Types import DefaultTypes, EasyTypes
from .. import Utils


class MessageHandler(Handler):
    """Обработчик текстовых сообщений"""

    async def Validate(self, obj: DefaultTypes.UpdateObject, **kwargs):
        return isinstance(obj, DefaultTypes.Message) and await super().Validate(obj, **kwargs)
    
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, bot, **kwargs):
        return super().GetPassedByType(obj, **kwargs) + [
            Utils.LazyObject(EasyTypes.Message, lambda: EasyTypes.Message(bot, obj))
        ]

class CallbackHandler(Handler):
    """Обработчик callback-запросов"""

    async def Validate(self, obj, **kwargs):
        return isinstance(obj, DefaultTypes.CallbackQuery) and await super().Validate(obj, **kwargs)
    
    def GetPassedByType(self, obj, **kwargs):
        return super().GetPassedByType(obj, **kwargs) + [
            obj
        ]
