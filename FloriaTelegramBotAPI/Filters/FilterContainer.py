from ..Types import DefaultTypes
from .BaseFilter import Filter
from .. import Validator


class FilterContainer:
    """Контейнер для группировки фильтров"""

    
    def __init__(self, *filters: Filter):
        self._filters = Validator.List(filters, Filter)
        
    async def Validate(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        for filter in self._filters:
            if not await filter(obj, **kwargs):
                return False
        return True