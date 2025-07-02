from typing import Any, Optional, TypeVar, Generic

from ..Storage import StorageContext
from .. import Validator
from .FSMModel import FSMModel, TFSMModel


class FSMContext(Generic[TFSMModel]):
    """Контекст FSM для управления состоянием и данными пользователя"""
    
    def __init__(
        self,
        context: StorageContext[TFSMModel],
    ):
        self._context: StorageContext[TFSMModel] = context

    async def GetModel(self):
        return await self._context.Get()

# data 
    async def GetData(self):
        return (await self._context.Get()).data
    
    async def UpdateData(self, **values):
        (await self.GetData()).update(**values)
    
    async def ClearData(self):
        (await self._context.Get()).data = {}
    
# state
    async def SetState(self, state):
        (await self._context.Get()).state = state
    
    async def ClearState(self):
        await self.SetState(None)
    
    async def GetState(self):
        return (await self._context.Get()).state

# both
    async def Clear(self):
        await self.ClearState()
        await self.ClearData()
    