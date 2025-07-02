from typing import Union, Optional, Any, Callable, Type, Literal, get_args, get_origin
from pydantic import BaseModel
import inspect
import os


def RemoveKeys(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    """Удалить данные из словаря по ключам

    Args:
        data (dict[str, Any]): Словарь

    Returns:
        dict[str, Any]: Новый словарь
    """
    return {
        key: value 
        for key, value in data.items()
        if key not in keys
    }

def RemoveValues(data: dict[str, Any], *values: Any) -> dict[str, Any]:
    """Удалить данные из словаря по значениям

    Args:
        data (dict[str, Any]): Словарь

    Returns:
        dict[str, Any]: Новый словарь
    """
    return {
        key: value
        for key, value in data.items()
        if value not in values
    }

def ToDict(**kwargs: Any) -> dict[str, Any]:
    return kwargs

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
    """Рекурсивно конвертировать примитивы и pydantic.BaseModel в json-формат

    Args:
        obj (Union[ dict[str, Any], list[Any], Any ]): Объект для конвертации

    Raises:
        RuntimeError: Неизвестный тип

    Returns:
        Union[ dict[str, Any], list[Any], Any ]: Конвертированный объект в json-формате
    """
    
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
        obj: BaseModel = obj
        return obj.model_dump(mode='json', exclude_none=True)
    
    elif obj.__class__ in [str, int, float, bool] or obj in [None]:
        return obj
    
    raise RuntimeError('Unsupport type')

def GetPathToObject(obj: Any) -> str:
    """Получить файл и линию объявления объекта

    Args:
        obj (Any): Объект

    Returns:
        str: Строчка формата 'File `_path_`, line `_number_`'
    """
    return f'File "{os.path.abspath(inspect.getfile(obj))}", line {inspect.getsourcelines(obj)[1]}'

class LazyObject:
    """Класс-обертка ленивого вызова функции-инициализации для работы совместно с `InvokeFunction`
    """
    
    def __init__(self, returning_type: Type, func: Callable[[], Any], *args, **kwargs):
        self.type = returning_type
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self):
        return self.func(*self.args, **self.kwargs)

async def InvokeFunction(
    func: Callable, 
    *,
    passed_by_name: dict[str, Any] = {}, 
    passed_by_type: list[Any | LazyObject] = []
) -> Any:
    """Вызов функции с передачей параметров по имени и типу

    Args:
        func (Callable): Сама функция
        passed_by_name (dict[str, Any]): Словарь для передачи параметров по имени
        passed_by_type (list[Any | LazyObject]): Словарь для передачи параметров по типу
        
    Raises:
        RuntimeError: Не удалось найти параметра для какого-то либо параметра функции

    Returns:
        Any: Результат выполнения функции
    """
    
    type_candidates = {}
    for value in passed_by_type:
        if value is None:
            continue
            
        if isinstance(value, LazyObject):
            type_candidates[value.type] = value
            
            if origin := get_origin(value.type):
                type_candidates[origin] = value
                
        else:
            obj_type = type(value)
            type_candidates[obj_type] = value
            
            if origin := get_origin(obj_type):
                type_candidates[origin] = value

    kwargs: dict[str, Any] = {}
    for key, ann_type in func.__annotations__.items():
        if key in passed_by_name:
            kwargs[key] = passed_by_name[key]
            continue
        
        try_types = []
        if get_origin(ann_type) is Union:
            try_types = [*get_args(ann_type)]
        else:
            try_types = [ann_type]
        
        for t in try_types.copy():
            origin = get_origin(t)
            if origin is not None:
                try_types.append(origin)
        
        value = None
        for t in try_types:
            if t in type_candidates:
                candidate = type_candidates[t]
                value = candidate() if isinstance(candidate, LazyObject) else candidate
                break
        
        if value is None:
            raise RuntimeError(f"""\n\tNo match for '{key}: {ann_type}' in function: \n\t{GetPathToObject(func)}""")
        
        kwargs[key] = value
        
    return await func(**kwargs)
