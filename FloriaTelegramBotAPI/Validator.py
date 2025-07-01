from typing import Type, Any, Callable, ParamSpecArgs, ParamSpecKwargs, TypeVar


T = TypeVar('T')


def List(data: list[Any], type: Type[T], *, subclass: bool = True) -> list[T]:
    for item in data:
        if subclass and not issubclass(item.__class__, type) or not subclass and not isinstance(item, type):
            raise ValueError()
    return [*data]

def ListTypes(data: list[Type[Any]], type: Type[T], *, subclass: bool = True) -> list[Type[T]]:
    for item in data:
        if subclass and not issubclass(item, type) or not subclass and not item is type:
            raise ValueError()
    return [*data]

def IsSubClass(data: Any, type: Type[T]) -> T:
    if not issubclass(data.__class__, type):
        raise ValueError()
    return data

def IsInstance(data: Any, type: Type[T]) -> T:
    if not isinstance(data, type):
        raise ValueError()
    return data

def ByFunc(func: Callable[[T], bool], data: T) -> T:
    if not func(data):
        raise ValueError()
    return data