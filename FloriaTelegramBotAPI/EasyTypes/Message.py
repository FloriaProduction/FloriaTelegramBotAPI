from typing import Optional, Union, Any

from .. import DefaultTypes, Utils, Enums, Validator
from ..Bot import Bot


class Message:
    def __init__(self, bot: 'Bot', message: DefaultTypes.MaybeInaccessibleMessage):
        Validator.IsInstance(bot, Bot)
        Validator.IsInstance(message, DefaultTypes.Message)
        
        self.bot: Bot = bot
        self.origin: DefaultTypes.MaybeInaccessibleMessage = message
    
    async def Send(
        self,
        text: str,
        reply_parameters: Optional[DefaultTypes.ReplyParameters] = None,
        reply_markup: Optional[Union[
            DefaultTypes.InlineKeyboardMarkup,
            DefaultTypes.ReplyKeyboardMarkup,
            DefaultTypes.ReplyKeyboardRemove,
            DefaultTypes.ForceReply
        ]] = None,
        parse_mode: Optional[Enums.ParseMode] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        **kwargs: Any
    ) -> 'Message': 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('chat_id', self.chat.id)
        
        return Message(self.bot, await self.bot.methods.SendMessage(**kwargs))
    
    async def Answer(
        self,
        text: str,
        reply_markup: Optional[Union[
            DefaultTypes.InlineKeyboardMarkup,
            DefaultTypes.ReplyKeyboardMarkup,
            DefaultTypes.ReplyKeyboardRemove,
            DefaultTypes.ForceReply
        ]] = None,
        parse_mode: Optional[Enums.ParseMode] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        **kwargs: Any
    ) -> 'Message':
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.update({
            'reply_parameters': DefaultTypes.ReplyParameters(
                message_id=self.id,
                chat_id=self.chat.id
            )
        })
        
        return await self.Send(**kwargs)

    async def EditText(
        self,
        text: str,
        reply_markup: Optional[DefaultTypes.InlineKeyboardMarkup] = None,
        parse_mode: Optional[Enums.ParseMode] = None,
        business_connection_id: Optional[str] = None,
        entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None,
        **kwargs: Any
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('chat_id', self.chat.id)
        kwargs.setdefault('message_id', self.id)
        
        return await self.bot.methods.EditMessageText(**kwargs)

    async def SendPhoto(
        self,
        photo: str | bytes,
        caption: Optional[str] = None,
        parse_mode: Optional[Enums.ParseMode] = None,
        caption_entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[DefaultTypes.ReplyParameters] = None,
        reply_markup: Optional[Union[
            DefaultTypes.InlineKeyboardMarkup,
            DefaultTypes.ReplyKeyboardMarkup,
            DefaultTypes.ReplyKeyboardRemove,
            DefaultTypes.ForceReply
        ]] = None,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        **kwargs: Any
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('chat_id', self.chat.id)
        
        return Message(self.bot, await self.bot.methods.SendPhoto(**kwargs))
    
    @property
    def text(self) -> Optional[str]:
        if isinstance(self.origin, DefaultTypes.Message):
            return self.origin.text
        return None
    
    @property
    def chat(self):
        return self.origin.chat
    
    @property
    def from_user(self) -> Optional[DefaultTypes.User]:
        if isinstance(self.origin, DefaultTypes.Message):
            return self.origin.from_user
        return None
    
    @property
    def id(self):
        return self.origin.message_id
    
    
    