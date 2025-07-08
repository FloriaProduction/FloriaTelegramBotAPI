from typing import Optional

from .. import DefaultTypes
from ..Bot import Bot


class CallbackQuery:
    def __init__(self, bot: Bot, query: DefaultTypes.CallbackQuery):
        self.bot: Bot = bot
        self.origin = query
    
    @property
    def data(self) -> Optional[str]:
        return self.origin.data