from .BaseFilter import Filter

from ..Types import DefaultTypes


class IsMessage(Filter):
    def Check(self, obj: DefaultTypes.Message, bot, **kwargs) -> bool:
        return isinstance(obj, DefaultTypes.Message)

class IsCommand(IsMessage):
    def Check(self, obj: DefaultTypes.Message, bot, **kwargs) -> bool:
        return super().Check(obj, bot, **kwargs) and len(obj.text) > 0 and obj.text[0] == '/'

class Command(IsCommand):
    def __init__(self, command: str):
        super().__init__()
        
        self.command = command
        
    def Check(self, obj: DefaultTypes.Message, bot, **kwargs):
        return super().Check(obj, bot, **kwargs) and obj.text[1:] == self.command

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
    def __init__(self, type: DefaultTypes.ChatType):
        super().__init__()
        self.type = type
    
    def Check(self, obj, bot, **kwargs):
        return obj.chat.type is self.type