from typing import overload

from ..Types import DefaultTypes
from ..Handlers import HandlerContainer, Handler, Handlers
from ..Filters.BaseFilter import Filter
from ..Filters.FilterContainer import FilterContainer
from ..Middleware import BaseMiddleware


class Router:
    def __init__(self, *filters: Filter):
        self._filters: FilterContainer = FilterContainer(*filters)
        self._handlers: HandlerContainer = HandlerContainer()
        self._routers: set[Router] = set()
    
    
    async def Processing(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        if self._filters.Validate(obj, bot, **kwargs):
            if await self._handlers.Invoke(obj, bot, **kwargs):
                return True
            
            for router in self._routers:
                if await router.Processing(obj, bot, **kwargs):
                    return True
            
        return False
            
    def Mount(self, router: 'Router'):
        self._routers.add(router)
    
    def Unmount(self, router: 'Router'):
        self._routers.remove(router)
    
    @property
    def middleware(self) -> BaseMiddleware:
        return self._handlers.middleware
    @middleware.setter
    def middleware(self, value: BaseMiddleware):
        self._handlers.middleware = value
        
    @overload
    def Callback(
        self,
        *filters: Filter
    ): ...
    
    def Callback(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(Handlers.CallbackHandler(*args, **kwargs), func)
        return wrapper
    
    @overload
    def Message(
        self,
        *filters: Filter
    ): ...
    
    def Message(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(Handlers.MessageHandler(*args, **kwargs), func)
        return wrapper
    
    @overload
    def Handler(
        self,
        *filters: Filter
    ): ...
    
    def Handler(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(Handler(*args, **kwargs), func)
        return wrapper
    
    def AddHandler(
        self, 
        handler: Handlers.Handler
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(handler, func)
        return wrapper
    
    