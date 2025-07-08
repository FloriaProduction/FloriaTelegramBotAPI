from typing import Any, Literal
from abc import ABC, abstractmethod

from .. import DefaultTypes


class Filter(ABC):
    @abstractmethod
    async def Check(self, obj: DefaultTypes.UpdateObject, **kwargs: Any) -> Any | Literal[False]:
        ...
