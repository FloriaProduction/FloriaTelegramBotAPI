import inspect
from typing import Callable, Union, Literal, Any

from .BaseHandler import Handler
from ..Middleware.BaseMiddleware import BaseMiddleware
from ..Types import DefaultTypes


class HandlerContainer:
    def __init__(self):
        self.handlers: list[Handler] = []
        self.middleware: BaseMiddleware = BaseMiddleware()
    
    def RegisterHandler(self, handler: Handler, func: Callable[[], Union[Literal[False], Any]], **kwargs) -> Callable[[], Union[Literal[False], Any]]:
        if not inspect.iscoroutinefunction(func):
            raise ValueError()
        
        if not issubclass(handler.__class__, Handler):
            raise ValueError()
        
        handler.func = func
        for key, value in kwargs.items():
            handler.__setattr__(key, value)
        self.handlers.append(handler)
        
        return func
    
    async def Invoke(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        for handler in self.handlers:
            if await self.middleware(handler, obj, bot, **kwargs):
                return True
        return False
    
    async def __call__(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return await self.Invoke(obj, bot, **kwargs)