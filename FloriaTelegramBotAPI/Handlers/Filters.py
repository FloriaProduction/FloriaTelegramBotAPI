from ..Types import DefaultTypes


class HandlerFilter:
    def Check(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        raise NotImplementedError()
        
    def __call__(self, obj: DefaultTypes.UpdateObject, bot, **kwargs) -> bool:
        return self.Check(obj, bot, **kwargs)

class IsMessage(HandlerFilter):
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

class Not(HandlerFilter):
    def __init__(self, filter: HandlerFilter):
        super().__init__()
        self.filter = filter
    
    def Check(self, obj, bot, **kwargs):
        return not self.filter(obj, bot, **kwargs)