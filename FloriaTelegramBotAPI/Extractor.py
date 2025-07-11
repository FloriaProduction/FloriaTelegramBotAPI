from typing import Literal

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

def GetExceptionText(exc: Exception, type: Literal['full', 'only_name'] = 'full') -> str:
    match type:
        case 'full':
            return f'Ошибка {exc.__class__.__name__}{
                f':\n  {'\n  '.join(map(str, exc.args))}' 
                if len(exc.args) > 0 else 
                ''
            }'
        
        case 'only_name':
            return f'Ошибка {exc.__class__.__name__}'
        
        case _:
            raise ValueError()