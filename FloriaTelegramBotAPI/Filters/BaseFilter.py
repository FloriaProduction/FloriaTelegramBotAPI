from ..Types import DefaultTypes


class Filter:
    """Базовый абстрактный класс для фильтров"""

    
    async def Check(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        raise NotImplementedError()
        
    async def __call__(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return await self.Check(obj, **kwargs)
