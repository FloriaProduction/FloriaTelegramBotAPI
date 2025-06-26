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
    def __init__(self, state: Enum):
        super().__init__()
        self.state: Enum = state
    
    def Check(self, obj, bot, state: Enum, **kwargs):
        return self.state is state

class InStates(Filters.HandlerFilter):
    def __init__(self, states: Type[Enum]):
        super().__init__()
        self.states: Type[Enum] = states
    
    def Check(self, obj, bot, state: Enum, **kwargs):
        return state in self.states._member_map_.values()

class FSMHanlder(Handlers.Handler):
    def __init__(self, *filters, **kwargs):
        super().__init__(*filters, **kwargs)
    
    def Validate(self, obj, bot, context: 'FSMContext', **kwargs):
        return super().Validate(
            obj, bot, 
            state=context.state,
            **kwargs
        )
    
    def GetPassedByType(self, obj, bot, context: 'FSMContext', fsm: 'FSM', **kwargs):
        return super().GetPassedByType(obj, bot, **kwargs) + [
            context,
            fsm
        ]

class FSMMessageHandler(Handlers.MessageHandler, FSMHanlder): pass


class FSMContext:
    def __init__(
        self,
        user_id: int,
        state: Enum,
        form: Optional[BaseModel] = None
    ):
        self._user_id = user_id
        self._state: Enum = state
        self.form = form

    @property
    def user_id(self):
        return self._user_id

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value: Enum):
        self._state = value


class FSM:
    def __init__(
        self,
        bot: Bot,
        cancel_command: str = 'cancel'
    ):
        self.bot: Bot = bot
        self._users: dict[int, FSMContext] = {}
        self._cancel_command: str = cancel_command
        
        self._handlers: HandlerContainer[FSMHanlder] = HandlerContainer()
        self._cancel_handlers: HandlerContainer[Handlers.Handler] = HandlerContainer()
        
        self.bot._handlers.RegisterHandler(Handlers.Handler(), self._Processing)
        
    async def _Processing(
        self,
        obj: DefaultTypes.UpdateObject,
        user: DefaultTypes.User
    ):
        context = self.GetContext(user.id)
        
        if context is None:
            return False
        
        if isinstance(obj, DefaultTypes.Message) and obj.text == f'/{self._cancel_command}':
            self.RemoveContext(user.id)
            return await self._cancel_handlers.Invoke(obj, self.bot)
        
        return await self._handlers.Invoke(
            obj, self.bot, 
            context=context,
            fsm=self
        )
        

    def GetContext(self, user_id: int) -> Optional[FSMContext]:
        return self._users.get(user_id)
    
    def CreateContext(self, user_id: int, state: Enum):
        self._users[user_id] = FSMContext(user_id, state)
    
    def SetContext(self, context: FSMContext):
        self._users[context.user_id] = context
    
    def HasContext(self, user_id: int) -> bool:
        return user_id in self._users
    
    def RemoveContext(self, user_id: int):
        self._users.pop(user_id, None)
    
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
            return self._handlers.RegisterHandler(FSMHanlder(*args, **kwargs), func)
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
            return self._handlers.RegisterHandler(FSMMessageHandler(*args, **kwargs), func)
        return wrapper
    
    def AddHandler(
        self, 
        handler: FSMHanlder
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(handler, func)
        return wrapper
    
    def AddCancelHandler(
        self, 
        handler: FSMHanlder
    ):
        def wrapper(func):
            return self._cancel_handlers.RegisterHandler(handler, func)
        return wrapper
