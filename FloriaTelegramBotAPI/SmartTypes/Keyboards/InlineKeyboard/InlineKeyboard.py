from typing import cast, Union, Optional

from .... import Utils, Types

from ..NewLine import NewLine


class InlineKeyboard:
    def __init__(
        self, 
        *buttons: Optional[Types.InlineKeyboardButton | NewLine]
    ):
        self.rows: list[list[Types.InlineKeyboardButton]] = []
        
        if buttons: self.Add(*buttons)
    
    def Add(self, *buttons: Optional[Types.InlineKeyboardButton | NewLine]):
        for button in buttons:
            if button is None:
                continue
            elif issubclass(button.__class__, NewLine) or isinstance(button, NewLine):
                self.rows.append([])
            else:
                self.rows[-1].append(button)
    
    def As_Markup(self) -> Types.InlineKeyboardMarkup:
        return Types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    button
                    for button in row
                ]
                for row in self.rows
            ]
        )