from ..Types import DefaultTypes


class Filter:
    def Check(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        raise NotImplementedError()
        
    def __call__(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return self.Check(obj, bot, **kwargs)
