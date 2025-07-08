from typing import Any, Generic

from .. import Abc
from ..Protocols.Functions import TCommonCallableAsync
from .. import Validator


class Event(Abc.Event[TCommonCallableAsync], Generic[TCommonCallableAsync]):
    def __init__(self):
        self._funcs: list[TCommonCallableAsync] = []
    
    def Register(self, func: TCommonCallableAsync):
        self._funcs.append(Validator.IsCallableAsync(func))
    
    async def Invoke(self, *args: Any, **kwargs: Any):
        for func in self._funcs:
            await func(*args, **kwargs)
