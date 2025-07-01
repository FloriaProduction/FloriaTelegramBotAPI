from typing import Iterable, Any, Type
from enum import Enum
import re

from .BaseFilter import Filter

from ..Types import DefaultTypes
from .. import Extractor, Enums, Validator


class IsMessage(Filter):
    def Check(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return isinstance(obj, DefaultTypes.Message)

class IsCommand(IsMessage):
    def Check(self, obj: DefaultTypes.Message, **kwargs) -> bool:
        return super().Check(obj, **kwargs) and obj.text is not None and len(obj.text) > 0 and obj.text[0] == '/'

class Command(IsCommand):
    def __init__(self, *commands: str):
        super().__init__()
        
        self._commands = Validator.List(commands, str, subclass=False)
        
    def Check(self, obj: DefaultTypes.Message, **kwargs):
        return super().Check(obj, **kwargs) and obj.text[1:] in self._commands


class IsCallback(Filter):
    def Check(self, obj: DefaultTypes.UpdateObject, **kwargs) -> bool:
        return isinstance(obj, DefaultTypes.CallbackQuery)


class Not(Filter):
    def __init__(self, filter: Filter):
        super().__init__()
        self._filter = Validator.IsSubClass(filter, Filter)
    
    def Check(self, obj, **kwargs):
        return not self._filter(obj, **kwargs)

class Or(Filter):
    def __init__(self, *filters: Filter):
        super().__init__()
        self._filters = Validator.List(filters, Filter)
    
    def Check(self, obj, **kwargs):
        for filter in self._filters:
            if filter(obj, **kwargs):
                return True
        return False


class Chat(Filter):
    def __init__(self, *types: Enums.ChatType):
        super().__init__()
        self._types = Validator.List(types, Enums.ChatType, subclass=False)
    
    def Check(self, obj, **kwargs):
        return Extractor.GetChat(obj).type in self._types

class InSequence(IsMessage):
    def __init__(self, *items: str, lower: bool = True):
        super().__init__()
        self._items = [
            item.lower()
            for item in items
        ] if lower else items
        self._lower = lower
    
    def Check(self, obj, **kwargs):
        return super().Check(obj, **kwargs) and obj.text is not None and (obj.text.lower() if self._lower else obj.text ) in self._items

class InEnum(InSequence):
    def __init__(self, *enums: Type[Enum], by_keys: bool = False, lower: bool = True):
        items = []
        for enum in Validator.List(enums, Type[Enum]):
            items += [
                key if by_keys else value.value
                for key, value in enum._member_map_.items()
            ]
        super().__init__(*items, lower=lower)

class Regex(IsMessage):
    def __init__(self, pattern: str):
        super().__init__()
        self._pattern = Validator.IsInstance(pattern, str)
    
    def Check(self, obj, **kwargs):
        return super().Check(obj, **kwargs) and obj.text is not None and re.fullmatch(self._pattern, obj.text) is not None