from typing import Optional, Union, Any

from .. import DefaultTypes
from ... import Utils

class Message:
    def __init__(self, bot, message: DefaultTypes.Message):
        from ...Bot import Bot
        
        self.origin: DefaultTypes.Message = message
        self.bot: Bot = bot
    
    async def SendMessage(
        self,
        text: str,
        reply_parameters: Optional[DefaultTypes.ReplyParameters] = None,
        reply_markup: Optional[Union[
            DefaultTypes.InlineKeyboardMarkup,
            DefaultTypes.ReplyKeyboardMarkup,
            DefaultTypes.ReplyKeyboardRemove,
            DefaultTypes.ForceReply
        ]] = None,
        parse_mode: Optional[str] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        **kwargs
    ): 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('chat_id', self.chat.id)
        
        await self.bot.methods.SendMessage(**kwargs)
    
    @property
    def text(self):
        return self.origin.text
    
    @property
    def chat(self):
        return self.origin.chat