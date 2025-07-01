from typing import Any, Optional, TypeVar
from pydantic import BaseModel

from .BaseStorage import Storage, NAME_TYPES, TBaseModel
from .. import Validator


class MemoryStorage(Storage[TBaseModel]):
    '''
    Обычное хранилище в ОЗУ
    '''
    
    def __init__(self, default: TBaseModel):
        super().__init__(default)

        self._records: dict[NAME_TYPES, TBaseModel] = {}
    
    async def Create(self, name: NAME_TYPES):
        self._records[name] = self._default_model.model_copy(deep=True)
    
    async def Get(self, name: NAME_TYPES):
        return self._records[name]
    
    async def Has(self, name: NAME_TYPES):
        return name in self._records

    async def Delete(self, name: NAME_TYPES):
        self._records.pop(name)

    