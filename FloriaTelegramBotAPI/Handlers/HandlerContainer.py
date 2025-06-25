import inspect
from typing import Callable, Union, Literal, Any, TypeVar, Generic

from .Handlers import Handler

_T = TypeVar('_T', bound=Handler)
class HandlerContainer(Generic[_T]):
    def __init__(self):
        self._handlers: list[_T] = []
        
    def RegisterHandler(self, handler: _T, func: Callable[[], Union[Literal[False], Any]], **kwargs) -> Callable[[], Union[Literal[False], Any]]:
        if not inspect.iscoroutinefunction(func):
            raise ValueError()
        
        handler.func = func
        for key, value in kwargs.items():
            handler.__setattr__(key, value)
        self._handlers.append(handler)
        
        return func
    
    async def Invoke(self, *args, **kwargs) -> bool:
        for handler in self._handlers:
            if await handler(*args, **kwargs):
                return True
        return False
    
    async def __call__(self, *args, **kwargs) -> bool:
        return await self.Invoke(*args, **kwargs)