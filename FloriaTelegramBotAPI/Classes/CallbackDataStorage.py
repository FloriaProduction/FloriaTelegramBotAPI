from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

from FloriaTelegramBotAPI import Exceptions
from .. import Abc
from ..Storages import MemoryStorage


class RecordData(BaseModel):
    data: str
    expires_at: datetime


class Storage:
    def __init__(self, storage: Optional[Abc.Storage[RecordData]] = None):
        self._storage: Abc.Storage[RecordData] = storage or MemoryStorage()
    
    def Register(self, data: str, life_time: timedelta = timedelta(minutes=20)) -> UUID:       
        token = uuid4()
        self._storage[token] = RecordData(
            data=data,
            expires_at=datetime.now() + life_time
        )
        return token

    def Get(self, token: str | UUID) -> str:
        if isinstance(token, str):
            try:
                token = UUID(token)
                
            except ValueError:
                raise Exceptions.CallbackStorageTokenNotValidError()
        
        try:
            record = self._storage[token]
            if record.expires_at <= datetime.now():
                self._storage.Pop(token)
                
            return record.data
        
        except KeyError:
            raise Exceptions.CallbackStorageTokenNotFoundError()
    
    # def Clear(self, all: bool = False):
    #     now = datetime.now()
    #     for name, data in self._callback_data_storage.Items():
    #         if all or data.expires_at <= now:
    #             del self._callback_data_storage[name]
    