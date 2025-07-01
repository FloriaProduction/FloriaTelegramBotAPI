import inspect
from typing import Callable, Union, Literal, Any, ParamSpecKwargs, Type

from .BaseHandler import Handler
from ..Middleware.BaseMiddleware import BaseMiddleware
from ..Types import DefaultTypes
from ..Mixin import Mixin
from .. import Validator


class HandlerContainer:
    """Контейнер для регистрации и вызова обработчиков"""

    def __init__(self):
        self._handlers: list[Handler] = []
        self._mixins: list[Type[Mixin]] = []
        self._middleware: BaseMiddleware = BaseMiddleware()
    
    def RegisterHandler(
        self, 
        func: Callable[[ParamSpecKwargs], Union[Literal[False], Any]], 
        handler: Handler, 
        *mixins: Type[Mixin], 
        **kwargs
    ) -> Callable[[ParamSpecKwargs], Union[Literal[False], Any]]:
        if not inspect.iscoroutinefunction(func):
            raise ValueError()
        
        handler = Validator.IsSubClass(handler, Handler)
        mixins = Validator.List(mixins, Type[Mixin])
        
        if self._mixins or mixins:
            handler.__class__ = type(f'{handler.__class__.__name__}_Mixed', (*self._mixins, *mixins, handler.__class__), {})
        
        handler._func = func
        for key, value in kwargs.items():
            handler.__setattr__(key, value)
        self._handlers.append(handler)
        
        return func
    
    async def Invoke(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        for handler in self._handlers:
            if await self._middleware(handler, obj, **kwargs):
                return True
        return False
    
    async def __call__(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return await self.Invoke(obj, **kwargs)
    
    @property
    def mixins(self) -> list[Type[Mixin]]:
        return self._mixins
    @mixins.setter
    def mixins(self, value: list[Type[Mixin]]):
        self._mixins = Validator.List(value, Mixin)
    
    @property
    def middleware(self) -> BaseMiddleware:
        return self._middleware
    @middleware.setter
    def middleware(self, value: BaseMiddleware):
        self._middleware = Validator.IsSubClass(value, BaseMiddleware)
    