import json
from typing import Union, Optional, Any, Callable, Type, get_args, get_origin, TypeVar, cast, Literal
from types import NoneType, UnionType
from pydantic import BaseModel
import inspect
import os
from . import Protocols, Types
import schedule


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
    obj: Types.PRIMITIVE_VALUES
) -> Types.JSON_TYPES:
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


async def InvokeFunction(
    func: Callable[..., Any], 
    *,
    passed_by_name: dict[str, Any] = {}, 
    passed_by_type: list[Any | LazyObject] = []
) -> Any:
    def _IsOptionalType(annotation: Any) -> bool:
        """Проверяет, содержит ли аннотация None или type(None)"""
        if annotation is None or annotation is NoneType:
            return True
            
        elif get_origin(annotation) is Union or isinstance(annotation, UnionType):
            return any(
                arg is None or arg is type(None) 
                for arg in get_args(annotation)
            )
        
        return False

    def _CollectTypeCandidates(
        passed_by_type: list[Any | LazyObject]
    ) -> dict[Type[Any], Any | LazyObject]:
        """Собирает словарь типов и их значений"""
        candidates: dict[Type[Any], Any | LazyObject] = {NoneType: None}
        
        for value in passed_by_type:
            if value is None:
                continue
                
            if isinstance(value, LazyObject):
                candidates[value.type] = value
                origin = get_origin(value.type)
                if origin is not None:
                    candidates[origin] = value
            else:
                obj_type = cast(Type[Any], type(value))
                candidates[obj_type] = value
                origin = get_origin(obj_type)
                if origin is not None:
                    candidates[origin] = value
                    
        return candidates

    def _ExpandAnnotationTypes(annotation: Any) -> set[Any]:
        """Раскрывает сложные типы аннотаций в плоский набор типов"""
        # Обработка Union и |
        
        types_set = set(get_args(annotation)) \
            if get_origin(annotation) is Union or isinstance(annotation, UnionType) else \
            {annotation}
        
        # Добавляем origin для каждого типа
        expanded: set[Any] = set()
        for type in types_set:
            expanded.add(type)
            origin = get_origin(type)
            if origin is not None:
                expanded.add(origin)
                
        return expanded

    def _FindValueForType(
        candidate_types: set[Any],
        type_candidates: dict[Type[Any], Any | LazyObject]
    ) -> Any:
        """Ищет подходящее значение для набора типов"""
        for type in candidate_types:
            if type in type_candidates:
                candidate = type_candidates[type]
                return candidate.Get() if isinstance(candidate, LazyObject) else candidate
        return None
    
    # Сбор доступных типов
    type_candidates = _CollectTypeCandidates(passed_by_type)
    signature = inspect.signature(func)
    kwargs = passed_by_name.copy()
    errors: list[str] = []
    
    # Обработка параметров функции
    for param_name, param in signature.parameters.items():
        if param_name in kwargs:
            continue
            
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
            
        ann = param.annotation
        if ann is param.empty:
            errors.append(f"Parameter '{param_name}' lacks type annotation")
            continue
        
        # Поиск значения
        value = _FindValueForType(
            _ExpandAnnotationTypes(ann), 
            type_candidates
        )
        
        # Обработка результатов
        if value is not None:
            kwargs[param_name] = value
        else:
            if param.default is not param.empty:
                continue  # Используем значение по умолчанию
            elif _IsOptionalType(ann):
                kwargs[param_name] = None  # Для Optional подставляем None
            else:
                # Формирование сообщения об ошибке
                base_types = get_args(ann) if get_origin(ann) is Union else {ann}
                type_names = [t.__name__ for t in base_types if t not in (None, type(None))]
                errors.append(f"{param_name}: {' | '.join(type_names)}")
    
    # Обработка ошибок
    if errors:
        available_types = ', '.join(t.__name__ for t in type_candidates)
        error_msg = "\n  - ".join(errors)
        raise RuntimeError(
            f"Failed to resolve arguments for function '{func.__name__}':\n  - {error_msg}\n"
            f"Available types: {available_types}"
        )
    
    return await func(**kwargs)

def ExceptionToText(exc: Exception, type: Literal['full', 'only_name'] = 'full') -> str:
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

def FileExists(path: str) -> bool:
    return os.path.exists(path)

def ReadFile(path: str, mode: Union[Literal['r', 'rb'], str] = 'r') -> str | bytes:
    with open(path, mode=mode, encoding='utf-8') as file:
        return file.read()

def WriteFile(path: str, data: Any):
    dir_path = os.path.dirname(path)
    if len(dir_path) > 0 and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
        
    with open(path, mode='w', encoding='utf-8') as file:
        file.write(f'{data}')

def ReadJson(path: str) -> Types.JSON_TYPES:
    return json.loads(ReadFile(path))

def WriteJson(path: str, data: Types.JSON_TYPES):
    WriteFile(path, json.dumps(data))
    
def AddEvery(seconds: int, func: Protocols.Functions.CommonCallable, *args: Any, **kwargs: Any):
    schedule.every(seconds).seconds.do(func, *args, **kwargs) # type: ignore

def Every(
    seconds: int
) -> Protocols.Functions.WrappedCommonCallable:
    def wrapper(func: Protocols.Functions.CommonCallable) -> Protocols.Functions.CommonCallable:
        AddEvery(seconds, func)
        return func
    return wrapper

