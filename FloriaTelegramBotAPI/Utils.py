from typing import Union, Optional, Any, Callable, Type
from pydantic import BaseModel
import inspect
import os


def RemoveKeys(data: dict[str, any], *keys: str) -> dict[str, any]:
    return {
        key: value 
        for key, value in data.items()
        if key not in keys
    }

def ConvertToJson(
    obj: Union[
        dict[str, Any],
        list[Any],
        Any
    ]
) -> Union[
    dict[str, Any],
    list[Any],
    Any
]:
    if isinstance(obj, dict):
        return {
            key: ConvertToJson(value)
            for key, value in obj.items()
        }
    
    elif isinstance(obj, list | tuple):
        return [
            ConvertToJson(value) 
            for value in obj
        ]
    
    elif issubclass(obj.__class__, BaseModel):
        # obj: BaseModel = obj
        return obj.model_dump(mode='json', exclude_none=True)
    
    elif obj.__class__ in [str, int, float, bool] or obj in [None]:
        return obj
    
    raise RuntimeError('Unsupport type')

def GetPathToObject(obj: Any):
    return f'File "{os.path.abspath(inspect.getfile(obj))}", line {inspect.getsourcelines(obj)[1]}'

class LazyObject:
    def __init__(self, returning_type: Type, func: Callable[[], Any], *args, **kwargs):
        self.type = returning_type
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self):
        return self.func(*self.args, **self.kwargs)

async def CallFunction(
    func: Callable, 
    *,
    passed_by_name: dict[str, Any] = {}, 
    passed_by_type: list[Any] = {}
):
    passed_by_type_dict = {}
    for value in passed_by_type:
        if value is None:
            continue
        type = None
        if issubclass(value.__class__, LazyObject):
            type = value.type
        else:
            type = value.__class__
        
        passed_by_type_dict[type] = value
        
    
    kwargs: dict[str, Any] = {}
    for key, type in func.__annotations__.items():
        if key in passed_by_name:
            kwargs[key] = passed_by_name[key]
        
        elif type in passed_by_type_dict:
            value = passed_by_type_dict[type]
            kwargs[key] = value() if issubclass(value.__class__, LazyObject) else value
        
        else:
            raise RuntimeError(f"""\n\tNo passed Name or Type found for field '{key}({type})' of function: \n\t{GetPathToObject(func)}""")
    
    return await func(**kwargs)

async def CallHandlers(
    handlers,
    *args,
    **kwargs
) -> bool:
    for handler in handlers:
        if await handler(*args, **kwargs):
            return True
    return False