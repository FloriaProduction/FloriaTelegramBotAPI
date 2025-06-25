from typing import Callable, Union, Literal, Any, overload

from .Filters import HandlerFilter
from ..Types import DefaultTypes, EasyTypes
from .. import Utils


class Handler:    
    def __init__(
        self,
        *filters: HandlerFilter,
        **kwargs: dict[str, Any]
    ):
        self.func: Callable[[], Union[Literal[False], Any]] = None
        self.args = Utils.Validator.List(HandlerFilter, filters)
        self.kwargs = kwargs
    
    def Validate(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        for filter in self.args:
            if not filter(obj, bot, **kwargs):
                return False
        return True
    
    @staticmethod
    def _GetUserFromUpdObj(obj: DefaultTypes.UpdateObject) -> DefaultTypes.User:
        if isinstance(obj, DefaultTypes.Message):
            return obj.from_user
        raise ValueError()
       
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> list[Any]:
        return [
            obj,
            bot,
            Utils.LazyObject(DefaultTypes.User, lambda: self._GetUserFromUpdObj(obj)),
        ]
    
    def GetPassedByName(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> dict[str, Any]:
        return {}

    async def Invoke(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        if self.Validate(obj, bot, **kwargs):
            return await Utils.InvokeFunction(
                self.func,
                passed_by_name=self.GetPassedByName(obj, bot, **kwargs),
                passed_by_type=self.GetPassedByType(obj, bot, **kwargs)
            ) is not False
        return False
        
    async def __call__(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return await self.Invoke(obj, bot, **kwargs)


class MessageHandler(Handler):
    def Validate(self, obj: DefaultTypes.UpdateObject, bot, **kwargs):
        return isinstance(obj, DefaultTypes.Message) and super().Validate(obj, bot, **kwargs)
    
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, bot, **kwargs):
        return super().GetPassedByType(obj, bot, **kwargs) + [
            Utils.LazyObject(EasyTypes.Message, lambda: EasyTypes.Message(bot, obj))
        ]
