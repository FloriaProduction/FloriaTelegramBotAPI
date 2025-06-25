import inspect
from typing import Callable, overload, TypeVar, Optional, Type, Generic
from enum import Enum
from pydantic import BaseModel

from ..Bot import Bot
from ..Handlers import Handlers, Filters, HandlerContainer
from ..Types import DefaultTypes
from .. import Utils


_TEnum = TypeVar('_TEnum', bound=Enum)


class State(Filters.HandlerFilter):
    def __init__(self, state: _TEnum):
        super().__init__()
        self.state = state
    
    def Check(self, obj, bot, state: _TEnum, **kwargs):
        return self.state is state


class FSMHanlder(Handlers.Handler):
    def __init__(self, *filters, **kwargs):
        super().__init__(*filters, **kwargs)
        
        self.fsm: FSM = None
    
    def Validate(self, obj, bot, **kwargs):
        context = self.fsm.GetContext(self._GetUserFromUpdObj(obj).id)
        return super().Validate(
            obj, bot, 
            state = context.state if context is not None else None,
            **kwargs
        )
    
    def GetPassedByType(self, obj, bot, **kwargs):
        return super().GetPassedByType(obj, bot, **kwargs) + [
            self.fsm,
            Utils.LazyObject(FSMContext, lambda: self.fsm.GetContext(self._GetUserFromUpdObj(obj).id))
        ]

class FSMMessageHandler(Handlers.MessageHandler, FSMHanlder): pass


class FSMContext(Generic[_TEnum]):
    def __init__(
        self,
        fsm: 'FSM',
        user_id: int,
        state: _TEnum
    ):
        self._fsm = fsm
        self._user_id = user_id
        self._state: _TEnum = state
    
    def SetState(self, state):
        self._state = state

    @property
    def state(self):
        return self._state


class FSM(Generic[_TEnum]):
    def __init__(
        self,
        bot: Bot,
    ):
        self.bot: Bot = bot
        self._users: dict[int, FSMContext[_TEnum]] = {}

    def GetContext(self, user_id: int) -> Optional[FSMContext]:
        return self._users.get(user_id)
    
    def CreateContext(self, user_id: int, state: _TEnum):
        self._users[user_id] = FSMContext(self, user_id, state)
    
    @overload
    def Handler(
        self,
        *filters: Handlers.HandlerFilter
    ): ...
    
    def Handler(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self.bot._handlers.RegisterHandler(
                FSMHanlder(*args, **kwargs), func, 
                fsm=self
            )
        return wrapper

    @overload
    def MessageHandler(
        self,
        *filters: Handlers.HandlerFilter
    ): ...
    
    def MessageHandler(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self.bot._handlers.RegisterHandler(
                FSMMessageHandler(*args, **kwargs), func, 
                fsm=self
            )
        return wrapper
    
    def AddHandler(
        self, 
        handler: FSMHanlder
    ):
        def wrapper(func):
            return self.bot._handlers.RegisterHandler(handler, func)
        return wrapper
