from typing import Optional, Type, Any
from pydantic import BaseModel
import json

from .... import DefaultTypes
from ..... import Utils


def InlineButton(
    text: str,
    callback_data: Optional[BaseModel] = None,
    copy_text: Optional[str] = None,
    url: Optional[str] = None,
    web_app: Optional[str] = None,
    login_url: Optional[DefaultTypes.LoginUrl] = None,
    switch_inline_query: Optional[str] = None,
    switch_inline_query_current_chat: Optional[str] = None,
    switch_inline_query_chosen_chat: Optional[DefaultTypes.SwitchInlineQueryChosenChat] = None,
    callback_game: Optional[str] = None,
    pay: Optional[bool] = None,
) -> DefaultTypes.InlineKeyboardButton:
    return DefaultTypes.InlineKeyboardButton(
        text=text,
        callback_data=Utils.MapOptional(callback_data, lambda data: data.model_dump_json() if issubclass(data.__class__, BaseModel) else json.dumps(data)),
        url=url,
        web_app=Utils.MapOptional(web_app, lambda data: DefaultTypes.WebAppInfo(data)),
        login_url=login_url,
        switch_inline_query=switch_inline_query,
        switch_inline_query_current_chat=switch_inline_query_current_chat,
        switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
        copy_text=Utils.MapOptional(copy_text, lambda data: DefaultTypes.CopyTextButton(text=data)),
        callback_game=callback_game,
        pay=pay
    )