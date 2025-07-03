from typing import Optional

from .... import DefaultTypes
from ..... import Utils, Validator

from ..NewLine import NewLine


class InlineKeyboard:
    def __init__(
        self, 
        *buttons: DefaultTypes.InlineKeyboardButton
    ):
        self.rows: list[list[DefaultTypes.InlineKeyboardButton]] = []
        
        if buttons: self.Add(*Validator.List(buttons, DefaultTypes.InlineKeyboardButton | NewLine))
    
    def Add(self, *buttons: DefaultTypes.InlineKeyboardButton):
        row = []
        for i, button in enumerate(buttons):
            if issubclass(button.__class__, NewLine):
                self.rows.append([*row])
                row.clear()
            else:
                row.append(button)
        if row:
            self.rows.append([*row])
    
    def As_Markup(self) -> DefaultTypes.InlineKeyboardMarkup:
        return DefaultTypes.InlineKeyboardMarkup(
            **Utils.RemoveValues(
                Utils.ToDict(
                    inline_keyboard=[
                        [
                            button
                            for button in row
                        ]
                        for row in self.rows
                    ]
                ),
                None
            )
        )