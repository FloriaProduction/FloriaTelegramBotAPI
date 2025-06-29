from typing import Any

from ..Handlers.BaseHandler import Handler
from ..Types import DefaultTypes


class BaseMiddleware:
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
        return await self.Invoke(handler, obj, bot, **kwargs)