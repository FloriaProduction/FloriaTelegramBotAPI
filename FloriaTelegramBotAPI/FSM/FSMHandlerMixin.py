from ..Mixin import Mixin
from ..Handlers.BaseHandler import Handler


class FSMHandlerMixin(Mixin, Handler):
    def GetPassedByType(self, obj, context, **kwargs):
        return super().GetPassedByType(obj, **kwargs) + [
            context
        ]