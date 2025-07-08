from typing import Any, cast

from .BaseHandler import Handler
from .. import Utils, DefaultTypes, EasyTypes
from ..Bot import Bot


class MessageHandler(Handler):
    async def Invoke(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool:
        if isinstance(obj, DefaultTypes.Message):
            return await super().Invoke(obj, **kwargs)
        return False

    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> list[Any]:
        bot: Bot = kwargs['bot']
        return super().GetPassedByType(obj, **kwargs) + [
            Utils.LazyObject(EasyTypes.Message, lambda: EasyTypes.Message(bot, cast(DefaultTypes.Message, obj)))
        ]

class CallbackHandler(Handler):
    async def Invoke(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool:
        if isinstance(obj, DefaultTypes.CallbackQuery):
            return await super().Invoke(obj, **kwargs)
        return False
    
    async def PostInvoke(self, result: bool, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool:
        bot: Bot = kwargs['bot']
        await bot.methods.AnswerCallbackQuery(
            callback_query_id=cast(DefaultTypes.CallbackQuery, obj).id
        )
        return result
    
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> list[Any]:
        bot: Bot = kwargs['bot']
        return super().GetPassedByType(obj, **kwargs) + [
            obj,
            Utils.MapOptional(
                cast(DefaultTypes.CallbackQuery, obj).message, 
                lambda msg: Utils.LazyObject(
                    EasyTypes.Message, 
                    lambda: EasyTypes.Message(
                        bot, 
                        msg
                    )
                )
            ),
            Utils.LazyObject(EasyTypes.CallbackQuery, lambda: EasyTypes.CallbackQuery(bot, cast(DefaultTypes.CallbackQuery, obj)))
        ]
    

