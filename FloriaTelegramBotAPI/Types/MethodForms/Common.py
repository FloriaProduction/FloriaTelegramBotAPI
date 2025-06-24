from pydantic import BaseModel, Field
from enum import Enum
from typing import Any, Optional, Union

from .. import DefaultTypes

class SendMessage(BaseModel):
    chat_id: int
    text: str
    reply_parameters: Optional[DefaultTypes.ReplyParameters] = None
    reply_markup: Optional[Union[
        DefaultTypes.InlineKeyboardMarkup,
        DefaultTypes.ReplyKeyboardMarkup,
        DefaultTypes.ReplyKeyboardRemove,
        DefaultTypes.ForceReply
    ]] = None
    parse_mode: Optional[str] = None
    business_connection_id: Optional[str] = None
    message_thread_id: Optional[int] = None
    entities: Optional[list[DefaultTypes.MessageEntity]] = None
    link_preview_options: Optional[DefaultTypes.LinkPreviewOptions] = None
    disable_notification: Optional[bool] = None
    protect_content: Optional[bool] = None
    allow_paid_broadcast: Optional[bool] = None
    message_effect_id: Optional[str] = None

    