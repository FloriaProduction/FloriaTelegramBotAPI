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
        row: list[Types.InlineKeyboardButton] = []
        for button in buttons:
            if button is None:
                continue
            elif issubclass(button.__class__, NewLine):
                self.rows.append([*row])
                row.clear()
            else:
                row.append(cast(Types.InlineKeyboardButton, button))
        if row:
            self.rows.append([*row])
    
    def As_Markup(self) -> Types.InlineKeyboardMarkup:
        return Types.InlineKeyboardMarkup(
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