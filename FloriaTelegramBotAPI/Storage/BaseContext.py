from typing import Optional, Any, TypeVar, Generic

from .BaseStorage import Storage, NAME_TYPES, TBaseModel


class StorageContext(Generic[TBaseModel]):
    '''
    Контекст для работы с записью хранилища
    '''
    
    def __init__(self, storage: Storage[TBaseModel], name: NAME_TYPES):
        self._storage: Storage[TBaseModel] = storage
        self._name = name

    @property
    def name(self):
        return self._name

    async def Get(self):
        return (await self._storage.GetOrCreate(self.name))