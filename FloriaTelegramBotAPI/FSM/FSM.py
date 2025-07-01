from typing import Generic, Optional

from ..Router import Router
from .. import Extractor
from ..Storage import Storage, StorageContext, MemoryStorage

from .FSMModel import FSMModel, TFSMModel
from .FSMContext import FSMContext
from .FSMHandlerMixin import FSMHandlerMixin


class FSM(Router, Generic[TFSMModel]):
    """Роутер с поддержкой конечного автомата (FSM)"""

    def __init__(self, *filters, storage: Optional[Storage[TFSMModel]] = None):
        super().__init__(*filters)
        self._handlers.mixins = [FSMHandlerMixin]
        
        self._storage: Storage[TFSMModel] = storage or MemoryStorage(FSMModel())
    
    def GetContext(self, user_id: int) -> FSMContext[TFSMModel]:
        return FSMContext(StorageContext(self._storage, user_id))
    
    async def Processing(self, obj, **kwargs):
        user = Extractor.GetUser(obj)
        context = self.GetContext(user.id)
        
        return await super().Processing(obj, context=context, **kwargs)
    