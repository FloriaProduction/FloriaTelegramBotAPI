from typing import Any

from ..Router import Router
from .. import Extractor

from .FSMContext import FSMContext
from .FSMHandlerMixin import FSMHandlerMixin

class FSM(Router):
    def __init__(self, *filters):
        super().__init__(*filters)
        self._handlers.mixins = [FSMHandlerMixin]
        
        self._users: dict[int, Any] = {}
    
    def Processing(self, obj, **kwargs):
        user = Extractor.GetUser(obj)
        context = self.GetOrCreateContext(user.id)
        
        return super().Processing(obj, context=context, **kwargs)
    
    def GetOrCreateContext(self, user_id: int) -> FSMContext:
        context = self._users.get(user_id)
        if context is None:
            context = FSMContext(user_id)
            self._users[user_id] = context
        return context
    