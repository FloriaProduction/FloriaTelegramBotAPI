from typing import Any
from abc import ABC, abstractmethod

from .. import DefaultTypes
from .. import Protocols


class Handler(ABC):
    @abstractmethod
    async def Validate(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool: ...

    @abstractmethod
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> list[Any]: ...
    
    @abstractmethod
    def GetPassedByName(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> dict[str, Any]: ...

    @abstractmethod
    async def Invoke(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool: ...
    
    @abstractmethod
    async def PostInvoke(self, result: bool, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> bool: ...
    
    @abstractmethod
    def SetFunction(self, func: Protocols.Functions.HandlerCallableAsync[...]): ...