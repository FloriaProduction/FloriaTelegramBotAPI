from typing import Optional, Union, Any, TypeVar
from enum import Enum
from pydantic import BaseModel


STATE_TYPE = Optional[Union[Enum, str, int]]
DATA_TYPE = Optional[dict[str, Any]]

class FSMModel(BaseModel):
    """Модель для хранения состояния и данных FSM"""

    state: STATE_TYPE = None
    data: DATA_TYPE = {}
    
TFSMModel = TypeVar('TFSMModel', bound=FSMModel)
