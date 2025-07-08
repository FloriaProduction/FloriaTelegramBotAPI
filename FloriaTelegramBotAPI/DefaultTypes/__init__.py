from typing import TypeVar, Union, Type
from uuid import UUID

from .Common import *


UpdateObject = Union[
    Message,
    CallbackQuery,
    Type[None]
]

TUpdateObject = TypeVar("TUpdateObject", bound=UpdateObject)
TUpdateObject_co = TypeVar("TUpdateObject_co", bound=UpdateObject, covariant=True)

KEY_TYPES = Union[
    str,
    int,
    UUID
]

PRIMITIVE_VALUES = Union[
    dict[str, 'PRIMITIVE_VALUES'],
    list['PRIMITIVE_VALUES'],
    str,
    int,
    float,
    bool,
    None,
    BaseModel
]
