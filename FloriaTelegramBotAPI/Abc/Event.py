from typing import Any, Generic
from abc import ABC, abstractmethod

from ..Protocols.Functions import TCommonCallableAsync


class Event(ABC, Generic[TCommonCallableAsync]):
    @abstractmethod
    def Register(self, func: TCommonCallableAsync):
        ...
    
    @abstractmethod
    async def Invoke(self, *args: Any, **kwargs: Any):
        ...
    
    async def __call__(self, *args: Any, **kwargs: Any):
        return await self.Invoke(*args, **kwargs)