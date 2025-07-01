from typing import overload

from ..Types import DefaultTypes
from ..Handlers import HandlerContainer, Handler, Handlers
from ..Filters.BaseFilter import Filter
from ..Filters.FilterContainer import FilterContainer
from ..Middleware import BaseMiddleware
from .. import Validator


class Router:
    """Маршрутизатор для обработки объектов обновлений"""

    def __init__(self, *filters: Filter):
        self._filters = FilterContainer(*filters)
        self._handlers = HandlerContainer()
        self._routers: list[Router] = []
    
    async def Processing(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        if await self._filters.Validate(obj, **kwargs):
            if await self._handlers.Invoke(obj, **kwargs):
                return True
            
            for router in self._routers:
                if await router.Processing(obj, **kwargs):
                    return True
            
        return False
            
    def Mount(self, router: 'Router'):
        if router in self._routers:
            raise ValueError()
        self._routers.append(Validator.IsSubClass(router, Router))
    
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
            return self._handlers.RegisterHandler(func, Handlers.CallbackHandler(*args, **kwargs))
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
            return self._handlers.RegisterHandler(func, Handlers.MessageHandler(*args, **kwargs))
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
            return self._handlers.RegisterHandler(func, Handler(*args, **kwargs))
        return wrapper
    
    def AddHandler(
        self, 
        handler: Handlers.Handler
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(func, handler)
        return wrapper
    
    