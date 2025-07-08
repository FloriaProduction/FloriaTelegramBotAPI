from pydantic import BaseModel
from typing import Optional, Union

from .. import Enums, DefaultTypes


class SendMessage(BaseModel):
    chat_id: str | int
    text: str
    reply_parameters: Optional[DefaultTypes.ReplyParameters] = None
    reply_markup: Optional[Union[
        DefaultTypes.InlineKeyboardMarkup,
        DefaultTypes.ReplyKeyboardMarkup,
        DefaultTypes.ReplyKeyboardRemove,
        DefaultTypes.ForceReply
    ]] = None
    parse_mode: Optional[Enums.ParseMode] = None
    business_connection_id: Optional[str] = None
    message_thread_id: Optional[int] = None
    entities: Optional[list[DefaultTypes.MessageEntity]] = None
    link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None


class SendChatAction(BaseModel):
    chat_id: str | int
    action: Enums.Action
    business_connection_id: Optional[str] = None
    message_thread_id: Optional[int] = None


class SendPhoto(BaseModel):
    chat_id: str | int
    photo: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[Enums.ParseMode] = None
    caption_entities: Optional[list[DefaultTypes.MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None
    reply_parameters: Optional[DefaultTypes.ReplyParameters] = None
    reply_markup: Optional[Union[
        DefaultTypes.InlineKeyboardMarkup,
        DefaultTypes.ReplyKeyboardMarkup,
        DefaultTypes.ReplyKeyboardRemove,
        DefaultTypes.ForceReply
    ]] = None
    business_connection_id: Optional[str] = None
    message_thread_id: Optional[int] = None


class AnswerCallbackQuery(BaseModel):
    callback_query_id: str
    text: Optional[str] = None
    show_alert: Optional[bool] = None
    url: Optional[str] = None
    cache_time: Optional[int] = None


class EditMessageText(BaseModel):
    text: str
    chat_id: Optional[str | int] = None
    reply_markup: Optional[DefaultTypes.InlineKeyboardMarkup] = None
    parse_mode: Optional[Enums.ParseMode] = None
    business_connection_id: Optional[str] = None
    message_id: Optional[int] = None
    inline_message_id: Optional[str] = None
    entities: Optional[list[DefaultTypes.MessageEntity]] = None
    link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None