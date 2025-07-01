from typing import Type, Any, Callable, ParamSpecArgs, ParamSpecKwargs, TypeVar, get_args, get_origin, Union


T = TypeVar('T')
T2 = TypeVar('T2')

def ByFunc(func: Callable[[T], bool], data: T) -> T:
    """Проверить объект при помощи передаваемой функции

    Args:
        func (Callable[[T], bool]): Функция валидации
        data (T): Объект

    Raises:
        ValueError: Объект не прошел проверку функцией

    Returns:
        T: Проверенный объект
    """
    if not func(data):
        raise ValueError()
    return data

def IsSubClass(data: Any | Type[Any], type_: Type[T]) -> T:
    """Объект является подклассом типа

    Args:
        data (Any | Type[Any]): Объект
        type_ (Type[T]): тип

    Raises:
        ValueError: Объект не является подклассом типа

    Returns:
        T: Проверенный объект
    """
    
    data_is_type = data.__class__ is type
    
    types = None
    if get_origin(type_) is Union:
        types = get_args(type_)
    else:
        types = (type_,)
    
    for cur_type in types:
        if issubclass(data if data_is_type else data.__class__, cur_type):
            return data
    raise ValueError()

def IsInstance(data: Any, type: Type[T]) -> T:  
    """Объект является экземпляром типа

    Args:
        data (Any | Type[Any]): Объект
        type (Type[T]): Тип

    Raises:
        ValueError: Объект не является экземпляром типа

    Returns:
        T: Проверенный объект
    """  
    
    types = None
    if get_origin(type) is Union:
        types = get_args(type)
    else:
        types = (type,)
    
    for cur_type in types:
        if isinstance(data, cur_type):
            return data
    raise ValueError()

def List(data: list[Any | Type[Any]], type: Type[T], *, subclass: bool = True) -> list[T]:
    """Элементы последовательности являются подклассом/экземпляром типа

    Args:
        data (list[Any  |  Type[Any]]): Последовательность
        type (Type[T]): Тип
        subclass (bool, optional): Если да, проверяет подкласс, иначе экземпляр. Defaults to True.

    Raises:
        ValueError: Элемент последовательности не является подклассом/экземпляром типа

    Returns:
        list[T]: Проверенная последовательность
    """
    
    for item in data:
        if subclass and not IsSubClass(item, type) or not subclass and not IsInstance(item, type):
            raise ValueError()
    return [*data]

def DictKeys(data: dict[Any, T2], type: Type[T], *, subclass: bool = True) -> dict[T2, T]:
    """Ключи словаря являются подклассом/экземпляром типа

    Args:
        data (dict[Any, T2]): Словарь
        type (Type[T]): Тип
        subclass (bool, optional): Если да, проверяет подкласс, иначе экземпляр. Defaults to True.

    Returns:
        dict[T2, T]: Проверенный словарь
    """
    
    List(data.keys(), type, subclass=subclass)
    return data

def DictValues(data: dict[T2, Any], type: Type[T], *, subclass: bool = True) -> dict[T2, T]:
    """Значения словаря являются подклассом/экземпляром типа

    Args:
        data (dict[Any, T2]): Словарь
        type (Type[T]): Тип
        subclass (bool, optional): Если да, проверяет подкласс, иначе экземпляр. Defaults to True.

    Returns:
        dict[T2, T]: Проверенный словарь
    """
    
    List(data.values(), type, subclass=subclass)
    return data

def Dict(data: dict[Any, Any], key_type: Type[T], value_type: Type[T2], *, subclass: bool = True) -> dict[T, T2]:
    """Ключи и значения словаря являются подклассом/экземпляром типов

    Args:
        data (dict[Any, Any]): Словарь
        key_type (Type[T]): Тип ключей
        value_type (Type[T2]): Тип значений
        subclass (bool, optional): Если да, проверяет подкласс, иначе экземпляр. Defaults to True.

    Returns:
        dict[T, T2]: Проверенный словарь
    """
    DictKeys(data, key_type, subclass=subclass)
    DictValues(data, value_type, subclass=subclass)
    return data

