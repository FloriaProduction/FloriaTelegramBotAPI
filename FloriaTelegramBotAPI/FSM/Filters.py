from typing import Any

from ..Filters.BaseFilter import Filter

from .FSMContext import FSMContext


class State(Filter):
    def __init__(self, *states: Any):
        super().__init__()
        self._states = states
    
    def Check(self, obj, context: FSMContext, **kwargs):
        return context.state in self._states
