from typing import Union, Optional, Any, Callable, Type, get_args, get_origin, TypeVar, cast
from types import UnionType
from pydantic import BaseModel
import inspect
import os
from . import Protocols


T = TypeVar("T")
T2 = TypeVar("T2")


def RemoveKeys(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {
        key: value 
        for key, value in data.items()
        if key not in keys
    }

def RemoveValues(data: dict[str, Any], *values: Any) -> dict[str, Any]:
    return {
        key: value
        for key, value in data.items()
        if value not in values
    }

def ToDict(**kwargs: Any) -> dict[str, Any]:
    return kwargs


def ConvertToJson(
    obj: Union[BaseModel, dict[str, Any], list[Any], str, int, float, bool, None]
) -> Union[dict[str, Any], list[Any], str, int, float, bool, None]:    
    if isinstance(obj, dict):
        return {
            key: ConvertToJson(value)
            for key, value in obj.items()
        }
    
    elif isinstance(obj, list):
        return [
            ConvertToJson(value) 
            for value in obj
        ]
    
    elif issubclass(obj.__class__, BaseModel):
        return cast(BaseModel, obj).model_dump(mode='json', exclude_none=True)
    
    elif isinstance(obj, Union[str, int, float, bool]) or obj in [None]:
        return obj
    
    raise RuntimeError('Unsupport type')

def GetPathToObject(obj: Any) -> str:
    return f'File "{os.path.abspath(inspect.getfile(obj))}", line {inspect.getsourcelines(obj)[1]}'

def MapOptional(data: Optional[T], func: Callable[[T], T2]) -> Optional[T2]:
    return None if data is None else func(data)

class LazyObject:
    def __init__(self, returning_type: Type[Any], func: Protocols.Functions.CommonCallable, *args: Any, **kwargs: Any):
        self.type: Type[Any] = returning_type
        self.func: Protocols.Functions.CommonCallable = func
        self.args = args
        self.kwargs = kwargs
    
    def Get(self):
        return self.func(*self.args, **self.kwargs)

# TODO: Разобраться в функции, оптимизировать
async def InvokeFunction(
    func: Protocols.Functions.HandlerCallableAsync[...], 
    *,
    passed_by_name: dict[str, Any] = {}, 
    passed_by_type: list[Any | LazyObject] = []
) -> Any:
    # 1. Собираем доступные типы в словарь
    type_candidates: dict[Type[Any], Any | LazyObject] = {
        type(None): None
    }
    
    for value in passed_by_type:
        if value is None:
            continue
            
        if isinstance(value, LazyObject):
            # Регистрируем основной тип и его origin (если есть)
            type_candidates[value.type] = value
            origin = get_origin(value.type)
            if origin is not None:
                type_candidates[origin] = value
        else:
            # Регистрируем конкретный тип и его origin
            obj_type: Type[Any] = cast(Type[Any], type(value))
            type_candidates[obj_type] = value
            origin = get_origin(obj_type)
            if origin is not None:
                type_candidates[origin] = value

    signature = inspect.signature(func)
    kwargs = passed_by_name.copy()
    errors: list[str] = []
    
    for param_name, param in signature.parameters.items():
        if param_name in kwargs:
            continue
            
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
            
        ann = param.annotation
        if ann is param.empty:
            errors.append(f"'{param_name}' is missing type annotation")
            continue
            
        candidate_types: set[Any] = set()
        
        if get_origin(ann) is Union or isinstance(ann, UnionType):
            candidate_types.update(get_args(ann))
        else:
            candidate_types.add(ann)
        
        additional_types: set[Any] = set()
        for t in candidate_types:
            origin = get_origin(t)
            if origin is not None:
                additional_types.add(origin)
        candidate_types.update(additional_types)
        
        value = None
        for t in candidate_types:
            if t in type_candidates:
                candidate = type_candidates[t]
                value = candidate.Get() if isinstance(candidate, LazyObject) else candidate
                break
        
        if value is not None:
            kwargs[param_name] = value
        elif param.default is param.empty:
            type_names = [t.__name__ for t in candidate_types]
            errors.append(f"{param_name}: {' | '.join(type_names)}")
    
    if errors:
        available_types = ', '.join(t.__name__ for t in type_candidates)
        error_msg = "\n  - ".join(errors)
        raise RuntimeError(
            f"Missing required arguments:\n  - {error_msg}\n"
            f"Available types: {available_types}"
        )
    
    return await func(**kwargs)
