from typing import Optional, Union

from .Types import DefaultTypes, MethodForms
from .WebClient import WebClient
from .Config import Config
from . import Validator, Utils, Enums


class BotMethods:
    def __init__(self, bot):
        from .Bot import Bot
        
        self._bot = Validator.IsSubClass(bot, Bot)
    
    @staticmethod
    def _ResponseToMessage(response) -> DefaultTypes.Message:
        return DefaultTypes.Message(**response['result'])
    
    async def SendMessage(
        self,
        chat_id: int,
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
    ) -> DefaultTypes.Message: 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('parse_mode', self._bot.config.parse_mode)
        
        return self._ResponseToMessage(
            await self.client.RequestPost(
                'sendMessage', 
                MethodForms.SendMessage(**kwargs)
            )
        )
    
    async def SendChatAction(
        self,
        chat_id: str | int,
        action: Enums.Action,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        **kwargs
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        await self.client.RequestPost(
            'sendChatAction',
            MethodForms.SendChatAction(**kwargs)
        )
    
    async def SendPhoto(
        self,
        chat_id: str | int,
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
        **kwargs
    ) -> DefaultTypes.Message:
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        
        response = None
        if isinstance(kwargs['photo'], str):
            response = await self.client.RequestPost(
                'sendPhoto',
                MethodForms.SendPhoto(**kwargs)
            ) 
        else: 
            photo_bytes = kwargs.pop('photo')
            response = await self.client.RequestPostData(
                'sendPhoto',
                MethodForms.SendPhoto(**kwargs),
                {
                    'photo': photo_bytes
                }
            ) 
        return self._ResponseToMessage(response)
    
    async def AnswerCallbackQuery(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None,
        **kwargs
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        await self.client.RequestPost(
            'answerCallbackQuery',
            MethodForms.AnswerCallbackQuery(**kwargs)
        )
    
    async def EditMessageText(
        self,
        text: str,
        chat_id: Optional[str | int] = None,
        reply_markup: Optional[DefaultTypes.InlineKeyboardMarkup] = None,
        parse_mode: Optional[Enums.ParseMode] = None,
        business_connection_id: Optional[str] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        entities: Optional[list[DefaultTypes.MessageEntity]] = None,
        link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None,
        **kwargs
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        await self.client.RequestPost(
            'editMessageText',
            MethodForms.EditMessageText(**kwargs)
        )
    
    @property
    def config(self) -> Config:
        return self._bot.config
    
    @property
    def client(self) -> WebClient:
        return self._bot.client