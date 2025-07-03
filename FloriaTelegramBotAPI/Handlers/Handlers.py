import json

from .BaseHandler import Handler
from ..Types import DefaultTypes, EasyTypes
from .. import Utils


class MessageHandler(Handler):
    """Обработчик текстовых сообщений"""

    async def Invoke(self, obj, **kwargs):
        if isinstance(obj, DefaultTypes.Message):
            return await super().Invoke(obj, **kwargs)
        return False
    
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, bot, **kwargs):
        return super().GetPassedByType(obj, **kwargs) + [
            Utils.LazyObject(EasyTypes.Message, lambda: EasyTypes.Message(bot, obj))
        ]

class CallbackHandler(Handler):
    """Обработчик callback-запросов"""

    async def Invoke(self, obj, **kwargs):
        if isinstance(obj, DefaultTypes.CallbackQuery):
            return await super().Invoke(
                obj, 
                **kwargs,
                callbackdata = EasyTypes.CallbackData(**json.loads(obj.data) if obj.data is not None and len(obj.data) > 0 else {})
            )
        return False

    async def PostInvoke(self, result, obj, **kwargs):
        await kwargs['bot'].methods.AnswerCallbackQuery(
            callback_query_id=obj.id
        )
        return result
    
    def GetPassedByType(self, obj: DefaultTypes.CallbackQuery, bot, callbackdata: dict, **kwargs):
        return super().GetPassedByType(obj, **kwargs) + [
            obj,
            Utils.LazyObject(EasyTypes.CallbackData, lambda: EasyTypes.CallbackData(callbackdata)),
            Utils.LazyObject(EasyTypes.Message, lambda: EasyTypes.Message(bot, obj.message))
        ]
    

