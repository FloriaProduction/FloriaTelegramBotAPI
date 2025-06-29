import inspect
from typing import Callable, Union, Literal, Any, TypeVar, Generic

from .BaseHandler import Handler
from ..Middleware.BaseMiddleware import BaseMiddleware
from ..Types import DefaultTypes


_T = TypeVar('_T', bound=Handler)
class HandlerContainer(Generic[_T]):
    def __init__(self):
        self._handlers: list[_T] = []
        self.middleware: BaseMiddleware = BaseMiddleware()
    
    def RegisterHandler(self, handler: _T, func: Callable[[], Union[Literal[False], Any]], **kwargs) -> Callable[[], Union[Literal[False], Any]]:
        if not inspect.iscoroutinefunction(func):
            raise ValueError()
        
        if not issubclass(handler.__class__, Handler):
            raise ValueError()
        
        handler.func = func
        for key, value in kwargs.items():
            handler.__setattr__(key, value)
        self._handlers.append(handler)
        
        return func
    
    async def Invoke(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        for handler in self._handlers:
            if await self.middleware(handler, obj, bot, **kwargs):
                return True
        return False
    
    async def __call__(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return await self.Invoke(obj, bot, **kwargs)