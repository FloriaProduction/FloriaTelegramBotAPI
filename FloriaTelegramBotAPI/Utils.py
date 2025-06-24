from typing import Union, Optional, Any, Callable
from pydantic import BaseModel


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


async def CallFunction(
    func: Callable, 
    *,
    passed_by_name: dict[str, Any] = {}, 
    passed_by_type: list[Any] = {}
):
    passed_by_type_dict = {
        value.__class__: value
        for value in passed_by_type
    }
    
    kwargs: dict[str, Any] = {}
    for key, type in func.__annotations__.items():
        if key in passed_by_name:
            kwargs[key] = passed_by_name[key]
        
        elif type in passed_by_type_dict:
            kwargs[key] = passed_by_type_dict[type]
        
        else:
            raise RuntimeError(f"No passed Name or Type found for field '{key}({type})'")
    
    return await func(**kwargs)
