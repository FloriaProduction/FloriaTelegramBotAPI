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
    
    passed_by_type_dict = {}
    for value in passed_by_type:
        if value is None:
            continue
        if issubclass(value.__class__, LazyObject):
            passed_by_type_dict[value.type] = value
        else:
            passed_by_type_dict[value.__class__] = value
        
    kwargs: dict[str, Any] = {}
    for key, type in func.__annotations__.items():
        if key in passed_by_name:
            kwargs[key] = passed_by_name[key]
            continue
        
        types_to_try = None
        if get_origin(type) is Union:
            types_to_try = get_args(type)
        else:
            types_to_try = (type,)
        
        for try_type in types_to_try:
            if try_type not in passed_by_type_dict:
                continue
            value = passed_by_type_dict[try_type]
            kwargs[key] = value() if issubclass(value.__class__, LazyObject) else value
            break
        
        else:
            raise RuntimeError(f"""\n\tNo passed Name or Type found for field '{key}({type})' of function: \n\t{GetPathToObject(func)}""")
        
    return await func(**kwargs)
