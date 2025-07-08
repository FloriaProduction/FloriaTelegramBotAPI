from typing import TypeVar, Union, Type

from .Common import *


UpdateObject = Union[
    Message,
    CallbackQuery,
    Type[None]
]

TUpdateObject = TypeVar("TUpdateObject", bound=UpdateObject)
TUpdateObject_co = TypeVar("TUpdateObject_co", bound=UpdateObject, covariant=True)
