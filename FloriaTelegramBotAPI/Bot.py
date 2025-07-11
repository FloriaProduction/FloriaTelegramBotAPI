from typing import Optional, Any
import logging
import schedule

from .Router import Router
from .Config import Config
from .Events import Event
from . import DefaultTypes
from .WebClient import WebClient
from .BotMethods import BotMethods
from . import Protocols, Validator


class Bot(Router):
    def __init__(self, token: str, config: Optional[Config] = None):
        super().__init__()
        
        self._config = config or Config()
        
        self._logger: Optional[logging.Logger] = None
        self._info: Optional[DefaultTypes.User] = None
        self._is_enabled: bool = True
        
        self._on_start_event: Event[Protocols.Functions.CommonCallableAsync] = Event()
        self._on_stop_event: Event[Protocols.Functions.CommonCallableAsync] = Event()
        
        self._update_offset: int = 0
        
        self._client: WebClient = WebClient(token, self._config)
        self._methods: BotMethods = BotMethods(self._config, self._client)


    async def Polling(self):
        self._info = DefaultTypes.User(**(await self._client.RequestGet('getMe'))['result'])
        
        self._logger = logging.getLogger(
            f'{self.info.username[:self.config.name_max_length]}{'..' if len(self.info.username) > self.config.name_max_length else ''}({self.info.id})'
            if self.info.username is not None else
            f'{self.info.first_name[:self.config.name_max_length]}{'..' if len(self.info.first_name) > self.config.name_max_length else ''}({self.info.id})'
        )
        
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self._config.stream_handler_level)
        stream_handler.setFormatter(logging.Formatter(self._config.log_format))
        self._logger.addHandler(stream_handler)
        
        if self._config.log_file is not None:
            file_handler = logging.FileHandler(self._config.log_file)
            file_handler.setLevel(self._config.file_handler_level)
            file_handler.setFormatter(logging.Formatter(self._config.log_format))
            self._logger.addHandler(file_handler)
        
        self._logger.setLevel(self._config.stream_handler_level)
        self.logger.info(f'Initialized')
        
        try:
            await self._on_start_event()
            
            while self.is_enabled:
                schedule.run_pending()
                for update in await self._client.GetUpdates(self._update_offset):
                    await self._ProcessUpdate(update)
            
        except:
            pass
        
        finally:
            await self._on_stop_event()
    
    def _SetUpdateOffset(self, offset: int):
        self._update_offset = max(self._update_offset, offset)
    
    async def _ProcessUpdate(self, update: dict[str, Any]):
        obj: Optional[DefaultTypes.UpdateObject] = None
        offset: int = 0
        try:
            offset = update.pop('update_id')
            
            for key, data in update.items():
                obj = self._ParseUpdateObject(key, data)
                if obj is None:
                    continue
                
                await self.Processing(
                    self._PostUpdateObject(obj), 
                    bot=self
                )
        
        except Exception as ex:
            if not (
                len(self._exceptions) > 0 and 
                await self._exceptions.Invoke(ex, obj=obj, bot=self)
            ):
                self.logger.error(ex.__class__.__name__, exc_info=True)
            
        finally:
            self._SetUpdateOffset(offset)
    
    def _ParseUpdateObject(self, key: str, data: dict[str, Any]) -> Optional[DefaultTypes.UpdateObject]:
        match key:
            case 'message':
                return DefaultTypes.Message(**data)
            
            case 'callback_query':
                return DefaultTypes.CallbackQuery(**data)
                
            case _:
                self.logger.warning(f'Unknowed update type: "{key}"')
                return None
    
    def _PostUpdateObject(self, obj: DefaultTypes.UpdateObject) -> DefaultTypes.UpdateObject:
        # if self._callback_data_storage is not None and isinstance(obj, Types.CallbackQuery) and obj.data is not None:
        #     obj.data = self._callback_data_storage.Get(obj.data)
        
        return obj
    
    @property
    def is_enabled(self) -> bool:
        return self._is_enabled
    def Stop(self):
        self._is_enabled = False
        
    @property
    def config(self) -> Config:
        return self._config

    @property
    def info(self) -> DefaultTypes.User:
        return Validator.IsNotNone(self._info)

    @property
    def logger(self) -> logging.Logger:
        return Validator.IsNotNone(self._logger)
    
    @property
    def methods(self):
        return self._methods
    
    def OnStart(self, func: Protocols.Functions.CommonCallableAsync):
        self._on_start_event.Register(func)
        return func
    
    def OnStop(self, func: Protocols.Functions.CommonCallableAsync):
        self._on_stop_event.Register(func)
        return func
