from typing import Callable, Union, Literal, Any

from .Filters import HandlerFilter
from ..Types import DefaultTypes, EasyTypes
from .. import Utils


class Handler:    
    def __init__(
        self,
        *filters: list[HandlerFilter],
        **kwargs: dict[str, Any]
    ):
        self.func = Callable[[], Union[Literal[False], Any]]
        self.args = filters
        self.kwargs = kwargs
    
    def Validate(self, bot, obj: DefaultTypes.UpdateObject) -> bool:
        for filter in self.args:
            if not filter(obj):
                return False
        return True
    
    def GetPassedByType(self, bot, obj: DefaultTypes.UpdateObject) -> list[Any]:
        return [
            obj,
            bot
        ]
    
    def GetPassedByName(self, bot, obj: DefaultTypes.UpdateObject) -> dict[str, Any]:
        return {}
    
    async def Call(self, bot, obj: DefaultTypes.UpdateObject) -> Any:
        return await Utils.CallFunction(
            self.func,
            passed_by_name=self.GetPassedByName(bot, obj),
            passed_by_type=self.GetPassedByType(bot, obj)
        )
    
    async def __call__(self, bot, obj: DefaultTypes.UpdateObject) -> bool:
        if self.Validate(bot, obj):
            return await self.Call(bot, obj) is not False


class MessageHandler(Handler):
    def Validate(self, bot, obj: DefaultTypes.UpdateObject) -> bool:
        return isinstance(obj, DefaultTypes.Message) and super().Validate(bot, obj)
    
    def GetPassedByType(self, bot, obj: DefaultTypes.UpdateObject) -> list[Any]:
        return super().GetPassedByType(bot, obj) + [
            EasyTypes.Message(bot, obj),
        ]
