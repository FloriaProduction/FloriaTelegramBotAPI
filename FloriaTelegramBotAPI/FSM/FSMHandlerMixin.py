from ..Mixin import Mixin
from ..Handlers.BaseHandler import Handler


class FSMHandlerMixin(Mixin, Handler):
    """Автоматически добавляет FSMContext в PassedByType"""

    def GetPassedByType(self, obj, context, **kwargs):
        return super().GetPassedByType(obj, **kwargs) + [
            context
        ]