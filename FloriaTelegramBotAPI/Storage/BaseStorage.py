from typing import Any, Optional, Union, TypeVar, Generic
from pydantic import BaseModel

from .. import Validator

NAME_TYPES = Union[
    str,
    int,
]

TBaseModel = TypeVar('TBaseModel', bound=BaseModel)
class Storage(Generic[TBaseModel]):   
    """
    Абстрактный класс Хранилища
    """
    
    def __init__(self, default: TBaseModel):
        self._default_model = Validator.IsSubClass(default, BaseModel)
        
    async def Create(self, name: NAME_TYPES):
        """Создать запись

        Args:
            name (NAME_TYPES): Уникальное имя записи
        """
        raise NotImplementedError()
    
    async def Get(self, name: NAME_TYPES) -> TBaseModel:
        """Получить запись

        Args:
            name (NAME_TYPES): Уникальное имя записи

        Returns:
            TBaseModel: Данные записи
        """
        raise NotImplementedError()
    
    async def Has(self, name: NAME_TYPES) -> bool:
        """Проверить наличие записи

        Args:
            name (NAME_TYPES): Уникальное имя записи

        Returns:
            bool: True если запись существует, иначе False
        """
        raise NotImplementedError()
    
    async def Delete(self, name: NAME_TYPES):
        """
        Удалить запись

        Args:
            name (NAME_TYPES): Уникальное имя записи
        """
        raise NotImplementedError()
    
    async def GetOrCreate(self, name: NAME_TYPES) -> TBaseModel:
        """Получить (или сначала создать) запись

        Args:
            name (NAME_TYPES): Уникальное имя записи

        Returns:
            TBaseModel: Данные записи
        """
        if not await self.Has(name):
            await self.Create(name)
        return await self.Get(name)
            
