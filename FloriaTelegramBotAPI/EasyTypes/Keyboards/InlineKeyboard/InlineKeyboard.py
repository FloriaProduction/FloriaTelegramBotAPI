from typing import cast, Union

from .... import DefaultTypes, Utils, Validator

from ..NewLine import NewLine


class InlineKeyboard:
    def __init__(
        self, 
        *buttons: DefaultTypes.InlineKeyboardButton | NewLine
    ):
        self.rows: list[list[DefaultTypes.InlineKeyboardButton]] = []
        
        if buttons: self.Add(*buttons)
    
    def Add(self, *buttons: Union[DefaultTypes.InlineKeyboardButton, NewLine]):
        row: list[DefaultTypes.InlineKeyboardButton] = []
        for button in Validator.List(buttons, DefaultTypes.InlineKeyboardButton, NewLine, subclass=False):
            if issubclass(button.__class__, NewLine):
                self.rows.append([*row])
                row.clear()
            else:
                row.append(cast(DefaultTypes.InlineKeyboardButton, button))
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