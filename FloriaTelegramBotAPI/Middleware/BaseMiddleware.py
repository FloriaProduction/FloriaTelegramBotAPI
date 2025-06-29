from typing import Any

from ..Handlers.BaseHandler import Handler
from ..Filters.BaseFilter import Filter
from ..Filters.FilterContainer import FilterContainer
from ..Types import DefaultTypes


class BaseMiddleware:
    def __init__(self, *filters: Filter):
        self._filters: FilterContainer = FilterContainer(*filters)
    
    async def Invoke(
        self,
        handler: Handler, 
        obj: DefaultTypes.UpdateObject,
        bot: Any,
        **kwargs
    ) -> bool:
        return await handler(obj, bot, **kwargs)
    
    async def __call__(
        self, 
        handler: Handler, 
        obj: DefaultTypes.UpdateObject,
        bot: Any,
        **kwargs
    ) -> bool:
        if self._filters.Validate(obj, bot):
            return await self.Invoke(handler, obj, bot, **kwargs)
        return False