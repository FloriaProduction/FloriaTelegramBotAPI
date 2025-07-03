from typing import Callable, Any

from ..BaseFilter import Filter
from ...Types import DefaultTypes
from ... import Validator


class IsCallback(Filter):
    """Фильтр для callback-запросов"""
    
    async def Check(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return isinstance(obj, DefaultTypes.CallbackQuery)

class CheckFields(IsCallback):
    def __init__(self, **values: Any | Callable[[Any], bool]):
        super().__init__()
        self._values = values
        
    async def Check(self, obj, callbackdata: dict, **kwargs):
        if not await super().Check(obj, **kwargs):
            return False
        
        for key, value in self._values.items():
            if key not in callbackdata or (not value(callbackdata[key]) if isinstance(value, Callable) else callbackdata[key] != value):
                return False
            
        return True