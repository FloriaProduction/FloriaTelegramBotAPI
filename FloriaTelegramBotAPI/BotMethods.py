from typing import Optional, Union, Any

from .WebClient import WebClient
from .Config import Config
from . import Utils, Enums, MethodForms, DefaultTypes



class BotMethods:
    def __init__(self, config: Config, client: WebClient):
        self._config: Config = config
        self._client: WebClient = client
    
    @staticmethod
    def _ResponseToMessage(response: dict[str, Any]) -> DefaultTypes.Message:
        return DefaultTypes.Message(**response['result'])
    
    # def _ReplaceCallbackData(self, markup: Types.InlineKeyboardMarkup) -> Types.InlineKeyboardMarkup:
    #     def SetCallbackData(button: Types.InlineKeyboardButton, new_data: str) -> Types.InlineKeyboardButton:
    #         button.callback_data = new_data
    #         return button
            
    #     markup.inline_keyboard = [
    #         [
    #             SetCallbackData(button, self._bot._callback_data_storage.Add(button.callback_data).hex) 
    #             if self._bot._callback_data_storage is not None and button.callback_data is not None else 
    #             button
    #             for button in line
    #         ]
    #         for line in markup.inline_keyboard
    #     ]
    #     return markup
    
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
        **kwargs: Any
    ) -> DefaultTypes.Message: 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        kwargs.setdefault('parse_mode', self.config.parse_mode)
        # if self._bot._callback_data_storage is not None and kwargs.get('reply_markup') is not None:
        #     kwargs['reply_markup'] = self._ReplaceCallbackData(kwargs['reply_markup'])
        
        
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
        **kwargs: Any
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
        **kwargs: Any
    ) -> DefaultTypes.Message: 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        # if self._bot._callback_data_storage is not None and kwargs.get('reply_markup') is not None:
        #     kwargs['reply_markup'] = self._ReplaceCallbackData(kwargs['reply_markup'])
        
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
        **kwargs: Any
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
        **kwargs: Any
    ):
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        # if self._bot._callback_data_storage is not None and kwargs.get('reply_markup') is not None:
        #     kwargs['reply_markup'] = self._ReplaceCallbackData(kwargs['reply_markup'])
        await self.client.RequestPost(
            'editMessageText',
            MethodForms.EditMessageText(**kwargs)
        )
    
    @property
    def config(self) -> Config:
        return self._config
    
    @property
    def client(self) -> WebClient:
        return self._client