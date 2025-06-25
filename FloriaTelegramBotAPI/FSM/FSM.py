import inspect
from typing import Callable, overload, TypeVar, Optional, Type
from enum import Enum

from ..Bot import Bot
from ..Handlers import Handlers, Filters
from ..Types import DefaultTypes
from .. import Utils


class FSMHanlder(Handlers.Handler):
    def __init__(self, state: Enum, *filters, **kwargs):
        super().__init__(*filters, **kwargs)
        self.state = state
        self.fsm: FSM = None
    
    def Validate(self, obj, bot, state, **kwargs):
        return state is self.state and super().Validate(obj, bot, **kwargs)
    
    def GetPassedByType(self, obj: DefaultTypes.UpdateObject, bot, state, **kwargs):
        return super().GetPassedByType(obj, bot, **kwargs) + [
            self.fsm,
            Utils.LazyObject(UserState, lambda: UserState(self.fsm, obj.from_user.id, state))
        ]

class FSMMessageHandler(Handlers.MessageHandler, FSMHanlder): pass

class UserState:
    def __init__(
        self,
        fsm: 'FSM',
        user_id: int,
        state: Enum
    ):
        self._fsm = fsm
        self._user_id = user_id
        self._state = state
    
    @property
    def user_id(self) -> int:
        return self._user_id
    
    @property
    def state(self) -> Enum:
        return self._state
    
    def SetState(self, state: Enum):
        self._fsm.SetState(self._user_id, state)
    
    def ClearState(self):
        self._fsm.ClearState(self._user_id)
    

class FSM:
    def __init__(
        self, 
        bot: Bot,
        states: Type[Enum],
        cancel_command: str = '/back'
    ):
        self.bot = bot
        self.states: Type[Enum] = states
        
        self._handlers: list[FSMHanlder] = []
        self._cancel_handlers: list[Handlers.Handler] = []
        self._user_states: dict[int, Enum] = {}
        
        self.cancel_command = cancel_command
        
        self.bot._RegisterHandler(Handlers.Handler(), self.Processing)
    
    async def Processing(
        self, 
        obj: DefaultTypes.UpdateObject, 
        bot: Bot, 
        user: DefaultTypes.User
    ):
        if self.GetState(user.id) is None:
            return False
        
        if isinstance(obj, DefaultTypes.Message) and obj.text == self.cancel_command:
            self.ClearState(user.id)
            return await Utils.CallHandlers(self._cancel_handlers, obj, bot, state=self.GetState(user.id))
        
        return await Utils.CallHandlers(self._handlers, obj, bot, state=self.GetState(user.id))
    
    def GetState(self, user_id: int) -> Optional[Enum]:
        return self._user_states.get(user_id)
    
    def SetState(self, user_id: int, state: Enum):
        if state not in self.states._member_map_.keys():
            raise ValueError()
        self._user_states[user_id] = state
    
    def ClearState(self, user_id: int):
        self._user_states.pop(user_id, None)
    
    def _RegisterHandler(self, handler: FSMHanlder, func: Callable) -> Callable:
        if not inspect.iscoroutinefunction(func):
            raise ValueError()
        
        handler.func = func
        handler.fsm = self
        self._handlers.append(handler)
        
        return func
    
    def _RegisterCancelHandler(self, handler: FSMHanlder, func: Callable) -> Callable:
        if not inspect.iscoroutinefunction(func):
            raise ValueError()
        
        handler.func = func
        self._cancel_handlers.append(handler)
        
        return func
    
    @overload
    def ExitHandler(
        self,
        *filters: Handlers.HandlerFilter
    ): ...
    
    def ExitHandler(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self._RegisterHandler(
                Handlers.Handler(
                    *args, 
                    **kwargs
                ), 
                func
            )
        return wrapper
    
    @overload
    def MessageHandler(
        self,
        state: Enum,
        *filters: Handlers.HandlerFilter
    ): ...
    
    def MessageHandler(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self._RegisterHandler(
                FSMMessageHandler(
                    args[0], 
                    *args[1:], 
                    **kwargs
                ), 
                func
            )
        return wrapper
    
    @overload
    def Handler(
        self,
        state: Enum,
        *filters: Handlers.HandlerFilter
    ): ...
    
    def Handler(
        self,
        *args,
        **kwargs
    ):
        def wrapper(func):
            return self._RegisterHandler(
                FSMHanlder(
                    args[0], 
                    *args[1:], 
                    **kwargs
                ), 
                func
            )
        return wrapper
    
    def AddCancelHandler(
        self,
        handler: Handlers.Handler
    ):
        def wrapper(func):
            return self._RegisterCancelHandler(handler, func)
        return wrapper
    
    def AddHandler(
        self, 
        handler: FSMHanlder
    ):
        def wrapper(func):
            return self._RegisterHandler(handler, func)
        return wrapper

        
    