from .BaseFilter import Filter
from .FilterContainer import FilterContainer

from .. import Extractor, Enums, Validator


class Not(Filter):
    """Инвертирует результат фильтра"""
    
    def __init__(self, filter: Filter):
        super().__init__()
        self._filter = Validator.IsSubClass(filter, Filter)
    
    async def Check(self, obj, **kwargs):
        return not await self._filter(obj, **kwargs)

class Or(Filter):
    """Проходит если ЛЮБОЙ из фильтров срабатывает"""
    
    def __init__(self, *filters: Filter):
        super().__init__()
        
        self._filters = FilterContainer(*filters)
    
    async def Check(self, obj, **kwargs):
        return await self._filters.Validate(obj, **kwargs)

class Chat(Filter):
    """Проверяет тип чата"""
    
    def __init__(self, *types: Enums.ChatType):
        super().__init__()
        self._types = Validator.List(types, Enums.ChatType, subclass=False)
    
    async def Check(self, obj, **kwargs):
        return Extractor.GetChat(obj).type in self._types

