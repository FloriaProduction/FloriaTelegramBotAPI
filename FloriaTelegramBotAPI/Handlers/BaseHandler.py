from typing import Callable, Union, Literal, Any, overload

from ..Filters.BaseFilter import Filter
from ..Filters.FilterContainer import FilterContainer
from ..Types import DefaultTypes
from .. import Utils


class Handler:    
    def __init__(
        self,
        *filters: Filter,
        **kwargs: dict[str, Any]
    ):
        self.func: Callable[[], Union[Literal[False], Any]] = None
        self.filters = FilterContainer(*filters)
        self.kwargs = kwargs
    
    def Validate(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return self.filters.Validate(obj, bot, **kwargs)

    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> list[Any]:
        return [
            obj,
            bot,
            Utils.LazyObject(DefaultTypes.User, lambda: Utils.Transformator.GetUser(obj)),
            Utils.LazyObject(DefaultTypes.Chat, lambda: Utils.Transformator.GetChat(obj)),
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


