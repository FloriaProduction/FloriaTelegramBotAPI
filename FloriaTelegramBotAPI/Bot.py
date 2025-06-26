from typing import Union, Iterable, overload, Callable, Optional, Any, Literal
import httpx
import inspect
import logging

from .Config import Config
from . import Utils, Exceptions, Enums
from .Types import DefaultTypes, MethodForms
from .Handlers import Handlers, Filters, HandlerContainer

class Bot:
    def __init__(self, token: str, config: Config = None):
        self._token = token
        self._config = config or Config()
        self._is_enabled = True
        
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        self._info: Optional[DefaultTypes.User] = None
        
        self._update_offset = 0
        
        self._handlers: HandlerContainer[Handlers.Handler] = HandlerContainer()
        
        self._logger: Optional[logging.Logger] = None
        
        self._methods: Optional[APIMethods] = None


    async def UpdateMe(self):
        self._info = DefaultTypes.User(**(await self._RequestGet('getMe')).json()['result'])
    
    async def Init(self):
        await self.UpdateMe()
        
        self._logger = logging.getLogger(f'{self._info.username[:self.config.name_max_length]}{'..' if len(self._info.username) > self.config.name_max_length else ''}({self._info.id})')
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._config.stream_handler_level)
        stream_handler.setFormatter(logging.Formatter(self._config.log_format))
        self.logger.addHandler(stream_handler)
        
        if self._config.log_file is not None:
            file_handler = logging.FileHandler(self._config.log_file)
            file_handler.setLevel(self._config.file_handler_level)
            file_handler.setFormatter(logging.Formatter(self._config.log_format))
            self.logger.addHandler(file_handler)
        
        self.logger.setLevel(self._config.stream_handler_level)
        self.logger.info(f'initialized')
        
        self._methods = APIMethods(self)
    
    async def Polling(self):
        await self.Init()
        
        while self.is_enabled:
            response = await self._RequestGet(
                'getUpdates', 
                {
                    'offset': self._update_offset + 1
                }
            )
            for update in response.json().get('result', []):
                try:
                    self.logger.debug(f'{update=}')
                    
                    self._update_offset = update.pop('update_id')
                    
                    for key, data in update.items():
                        obj = None
                        match key:
                            case 'message':
                                obj = DefaultTypes.Message(**data)
                            
                            case _:
                                self.logger.warning(f'Unknowed Update: "{key}": {data}')
                                continue
                        
                        if await self._handlers(obj, self):
                            break

                except BaseException as ex:
                    if False:
                        pass
                    else:
                        self.logger.error(ex.__class__.__name__, exc_info=True)
                
                finally:
                    pass
        
        await self._RequestGet('getUpdates', { 'offset': self._update_offset + 1 })
    
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
            return self._handlers.RegisterHandler(Handlers.MessageHandler(*args, **kwargs), func)
        return wrapper
    
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
            return self._handlers.RegisterHandler(Handlers.Handler(*args, **kwargs), func)
        return wrapper
    
    def AddHandler(
        self, 
        handler: Handlers.Handler
    ):
        def wrapper(func):
            return self._handlers.RegisterHandler(handler, func)
        return wrapper
    
    async def _makeRequest(
        self, 
        method: Callable, 
        command: str,
        **kwargs
    ) -> httpx.Response:
        current_attempt_count = 0
        while current_attempt_count < self.config.retry_count:
            try:
                response: httpx.Response = await method(
                    url=f'https://api.telegram.org/bot{self._token}/{command}',
                    **kwargs
                )
                if not response.is_success:
                    data: dict = response.json()
                    raise Exception(f'\n\tCode: {data.get('error_code')}\n\tDescription: {data.get('description')}\n\tCommand: {command}\n\tRequest: {response.request.content}')
                
                return response
                
            except:
                self.logger.warning('', exc_info=True)
            
            finally:
                current_attempt_count += 1
        
        raise httpx.RequestError(f'Failed to complete request after {self.config.retry_count} attempts')
        
    async def _RequestGet(
        self, 
        command: str, 
        data: Optional[Any] = None
    ) -> httpx.Response:
        return await self._makeRequest(
            self._client.get, 
            command,
            
            params=Utils.ConvertToJson(data or {})
        )
    
    async def _RequestPost(
        self, 
        command: str, 
        data: Any
    ) -> httpx.Response:
        return await self._makeRequest(
            self._client.post, 
            command,
            
            json=Utils.ConvertToJson(data or {}),
        )

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled
    def Stop(self):
        self._is_enabled = False
        
    @property
    def config(self) -> Config:
        return self._config
    
    @property
    def logger(self) -> logging.Logger:
        if self._logger is None: raise Exceptions.NotInitializedError()
        return self._logger

    @property
    def info(self) -> DefaultTypes.User:
        if self._info is None: raise Exceptions.NotInitializedError()
        return self._info
    
    @property
    def methods(self):
        if self._methods is None: raise Exceptions.NotInitializedError()
        return self._methods

# API

class APIMethods:
    def __init__(self, bot: 'Bot'):
        self.bot = bot
    
    async def SendMessage(
        self,
        chat_id: int,
        text: str,
        reply_parameters: Optional[DefaultTypes.ReplyParameters] = None,
        reply_markup: Optional[Union[
            DefaultTypes.InlineKeyboardMarkup,
            DefaultTypes.ReplyKeyboardMarkup,
            DefaultTypes.ReplyKeyboardRemove,
            DefaultTypes.ForceReply
        ]] = None,
        parse_mode: Optional[str] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        **kwargs
    ): 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('parse_mode', self.bot.config.parse_mode)
        
        await self.bot._RequestPost(
            'sendMessage',
            MethodForms.SendMessage(**kwargs)
        )
    
    async def SendChatAction(
        self,
        chat_id: str | int,
        action: Enums.Action,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        **kwargs
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        await self.bot._RequestPost(
            'sendChatAction',
            MethodForms.SendChatAction(**kwargs)
        )
