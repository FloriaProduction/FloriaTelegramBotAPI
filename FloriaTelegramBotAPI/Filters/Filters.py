from .BaseFilter import Filter

from ..Types import DefaultTypes
from .. import Enums


class IsMessage(Filter):
    def Check(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return isinstance(obj, DefaultTypes.Message)

class IsCommand(IsMessage):
    def Check(self, obj: DefaultTypes.Message, bot, **kwargs) -> bool:
        return super().Check(obj, bot, **kwargs) and obj.text is not None and len(obj.text) > 0 and obj.text[0] == '/'

class Command(IsCommand):
    def __init__(self, command: str):
        super().__init__()
        
        self.command = command
        
    def Check(self, obj: DefaultTypes.Message, bot, **kwargs):
        return super().Check(obj, bot, **kwargs) and obj.text[1:] == self.command


class IsCallback(Filter):
    def Check(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return isinstance(obj, DefaultTypes.CallbackQuery)


class Not(Filter):
    def __init__(self, filter: Filter):
        super().__init__()
        self.filter = filter
    
    def Check(self, obj, bot, **kwargs):
        return not self.filter(obj, bot, **kwargs)

class Or(Filter):
    def __init__(self, *filters: Filter):
        super().__init__()
        self.filters = filters
    
    def Check(self, obj, bot, **kwargs):
        for filter in self.filters:
            if filter(obj, bot, **kwargs):
                return True
        return False


class Chat(Filter):
    def __init__(self, *types: Enums.ChatType):
        super().__init__()
        self.types = types
    
    def Check(self, obj, bot, **kwargs):
        if isinstance(obj, DefaultTypes.Message):
            return obj.chat.type in self.types
        elif isinstance(obj, DefaultTypes.CallbackQuery):
            return obj.message.chat.type in self.types
        raise ValueError()
