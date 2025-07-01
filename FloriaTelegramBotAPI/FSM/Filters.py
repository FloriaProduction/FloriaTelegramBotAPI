from ..Filters.BaseFilter import Filter

from .FSMModel import STATE_TYPE
from .FSMContext import FSMContext


class State(Filter):
    """Проверяет текущее состояние FSM для пользователя"""

    def __init__(self, *states: STATE_TYPE):
        super().__init__()
        self._states = states
    
    async def Check(self, obj, context: FSMContext, **kwargs):
        return await context.GetState() in self._states
