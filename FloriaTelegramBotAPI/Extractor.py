from . import Validator, DefaultTypes


def GetUser(obj: DefaultTypes.UpdateObject) -> DefaultTypes.User:
    if isinstance(obj, DefaultTypes.Message):
        return Validator.IsNotNone(obj.from_user)
    
    elif isinstance(obj, DefaultTypes.CallbackQuery):
        return obj.from_user
    
    raise ValueError()


def GetChat(obj: DefaultTypes.UpdateObject) -> DefaultTypes.Chat:
    if isinstance(obj, DefaultTypes.Message):
        return obj.chat
    
    elif isinstance(obj, DefaultTypes.CallbackQuery):
        return Validator.IsNotNone(obj.message).chat
    
    raise ValueError()