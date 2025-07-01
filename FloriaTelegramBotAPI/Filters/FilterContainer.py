from ..Types import DefaultTypes
from .BaseFilter import Filter
from .. import Validator


class FilterContainer:
    def __init__(self, *filters: Filter):
        self._filters = Validator.List(filters, Filter)
        
    def Validate(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        for filter in self._filters:
            if not filter(obj, **kwargs):
                return False
        return True