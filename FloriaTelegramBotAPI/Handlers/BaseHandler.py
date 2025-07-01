from typing import Callable, Union, Literal, Any, overload, ParamSpecKwargs

from ..Filters.BaseFilter import Filter
from ..Filters.FilterContainer import FilterContainer
from ..Types import DefaultTypes
from .. import Extractor, Utils


class Handler:    
    def __init__(
        self,
        *filters: Filter,
        **kwargs: dict[str, Any]
    ):
        self._func: Callable[[], Union[Literal[False], Any]] = lambda *args, **kwargs: print(f'Empty handler function')
        self._filters = FilterContainer(*filters)
        self._kwargs = kwargs
    
    def Validate(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return self._filters.Validate(obj, **kwargs)

    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, **kwargs) -> list[Any]:
        return [
            obj,
            kwargs.get('bot'),
            Utils.LazyObject(DefaultTypes.User, lambda: Extractor.GetUser(obj)),
            Utils.LazyObject(DefaultTypes.Chat, lambda: Extractor.GetChat(obj)),
        ]
    
    def GetPassedByName(self, obj: DefaultTypes.UpdateObject, **kwargs) -> dict[str, Any]:
        return {}

    async def Invoke(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        if self.Validate(obj, **kwargs):
            return await Utils.InvokeFunction(
                self._func,
                passed_by_name=self.GetPassedByName(obj, **kwargs),
                passed_by_type=self.GetPassedByType(obj, **kwargs)
            ) is not False
        return False
        
    async def __call__(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return await self.Invoke(obj, **kwargs)
