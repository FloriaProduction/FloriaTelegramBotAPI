from typing import Union, Callable, Optional, Any
import httpx
import logging

from .Config import Config
from . import Utils, Exceptions, Enums
from .Types import DefaultTypes, MethodForms
from .Router import Router
from . import Validator
from .WebClient import WebClient
from .BotMethods import BotMethods


class Bot(Router):
    def __init__(self, token: str, config: Optional[Config] = None):
        super().__init__()
        
        self._config = Validator.IsSubClass(config, Config | None) or Config()
        
        self._client = WebClient(token, self)
        self._methods: Optional[BotMethods] = None
        
        self._logger: Optional[logging.Logger] = None
        
        self._info: Optional[DefaultTypes.User] = None
        self._is_enabled = True
        
        self._update_offset: int = 0
        
    async def Init(self):
        self._info = DefaultTypes.User(**(await self._client.RequestGet('getMe'))['result'])
        
        self._logger = logging.getLogger(f'{self.info.username[:self.config.name_max_length]}{'..' if len(self.info.username) > self.config.name_max_length else ''}({self.info.id})')
        
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
        
        self._methods = BotMethods(self)
    
    async def Polling(self, *, skip_updates: bool = False):
        await self.Init()
        
        if skip_updates:
            await self._client.GetUpdates(self._update_offset)
        
        while self.is_enabled:
            for update in await self._client.GetUpdates(self._update_offset):
                try:
                    self.logger.debug(f'{update=}')
                    
                    self._update_offset = update.pop('update_id')
                    
                    for key, data in update.items():
                        obj = None
                        match key:
                            case 'message':
                                obj = DefaultTypes.Message(**data)
                            
                            case 'callback_query':
                                obj = DefaultTypes.CallbackQuery(**data)
                            
                            case _:
                                self.logger.warning(f'Unknowed Update: "{key}": {data}')
                                continue
                        
                        await self.Processing(obj, bot=self)

                except BaseException as ex:
                    if False:
                        pass
                    else:
                        self.logger.error(ex.__class__.__name__, exc_info=True)
                
                finally:
                    pass
    
    @property
    def is_enabled(self) -> bool:
        return self._is_enabled
    def Stop(self):
        self._is_enabled = False
        
    @property
    def config(self) -> Config:
        return self._config
    
    @property
    def client(self) -> WebClient:
        return self._client
    
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
 
