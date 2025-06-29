from ..Types import DefaultTypes
from .BaseFilter import Filter
from .. import Utils


class FilterContainer:
    def __init__(self, *filters: Filter):
        self.filters: list[Filter] = Utils.Validator.List(Filter, filters)
        
    def Validate(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        for filter in self.filters:
            if not filter(obj, bot, **kwargs):
                return False
        return True