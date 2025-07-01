from .BaseMiddleware import BaseMiddleware
from ..Types import DefaultTypes
from .. import Extractor


class ErrorLoggerMiddleware(BaseMiddleware):
    """Логирует ошибки обработчиков"""

    async def Invoke(self, handler, obj, **kwargs):
        try:
            return await super().Invoke(handler, obj, **kwargs)
        
        except BaseException:
            from ..Bot import Bot
            
            bot: Bot = kwargs.get('bot')
            user: DefaultTypes.User = Extractor.GetUser(obj)
                
            bot.logger.error(f'{user.username}:', exc_info=True)
        
            return False
