from typing import Any, Type
from abc import ABC, abstractmethod

from .. import DefaultTypes
from .Handler import Handler
from .. import Protocols


class Router(ABC):
    @abstractmethod
    async def Processing(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool: ...
    
    @abstractmethod
    def Mount(self, router: 'Router'): ...
    
    @abstractmethod
    def AddHandler(self, handler: Handler) -> Protocols.Functions.WrapperHandlerCallable: ...
    
    @abstractmethod
    def Exception(self, exception: Type[Exception]) -> Protocols.Functions.WrapperExceptionCallable: ...
    
    @abstractmethod 
    def __len__(self) -> int: ...
