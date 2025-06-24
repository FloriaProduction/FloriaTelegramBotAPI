from ..Types import DefaultTypes


class HandlerFilter:
    def __init__(self):
        pass
    
    def Check(self, obj: DefaultTypes.UpdateObject) -> bool:
        raise NotImplementedError()
        
    def __call__(self, obj: DefaultTypes.UpdateObject) -> bool:
        return self.Check(obj)

class IsMessage(HandlerFilter):
    def Check(self, obj: DefaultTypes.Message) -> bool:
        return isinstance(obj, DefaultTypes.Message)

class IsCommand(IsMessage):
    def Check(self, obj: DefaultTypes.Message) -> bool:
        return super().Check(obj) and len(obj.text) > 0 and obj.text[0] == '/'

class Command(IsCommand):
    def __init__(self, command: str):
        super().__init__()
        
        self.command = command
        
    def Check(self, obj):
        return super().Check(obj) and obj.text[1:] == self.command