from typing import Optional, Union, Any

from .WebClient import WebClient
from .Config import Config
from . import Utils, Enums, MethodForms, DefaultTypes
from .Classes import CallbackDataStorage



class BotMethods:
    def __init__(self, config: Config, client: WebClient):
        self._config: Config = config
        self._client: WebClient = client
        
        self._callback_data_storage = CallbackDataStorage.Storage() if self.config.callback_length_fix is not False else None
    
    @staticmethod
    def _ResponseToMessage(response: dict[str, Any]) -> DefaultTypes.Message:
        return DefaultTypes.Message(**response['result'])
    
    def _ReplaceCallbackData(self, markup: Optional[DefaultTypes.InlineKeyboardMarkup]) -> Optional[DefaultTypes.InlineKeyboardMarkup]:
        def SetCallbackData(button: DefaultTypes.InlineKeyboardButton, data: str) -> DefaultTypes.InlineKeyboardButton:
            button.callback_data = data
            return button
        
        if self._callback_data_storage is None or markup is None:
            return markup
        
        markup.inline_keyboard = [
            [
                SetCallbackData(
                    button, 
                    self.callback_data_storage.Register(button.callback_data).hex
                ) 
                if button.callback_data is not None else 
                button
                for button in line
            ]
            for line in markup.inline_keyboard
        ]
        return markup
    
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
    ) -> DefaultTypes.Message: 
        kwargs.update(Utils.RemoveKeys(locals(), 'self', 'kwargs'))
        if kwargs['parse_mode'] is None:
            kwargs['parse_mode'] = self.config.parse_mode
        kwargs['reply_markup'] = self._ReplaceCallbackData(kwargs['reply_markup'])
        
        
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
        if kwargs['parse_mode'] is None:
            kwargs['parse_mode'] = self.config.parse_mode
        kwargs['reply_markup'] = self._ReplaceCallbackData(kwargs['reply_markup'])
        
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
        if kwargs['parse_mode'] is None:
            kwargs['parse_mode'] = self.config.parse_mode
        kwargs['reply_markup'] = self._ReplaceCallbackData(kwargs['reply_markup'])
        
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
    
    @property
    def callback_data_storage(self) -> CallbackDataStorage.Storage:
        if self._callback_data_storage is None:
            raise RuntimeError()
        return self._callback_data_storage
    
    @property
    def callback_data_length_fix_enabled(self) -> bool:
        return self._callback_data_storage is not None
        