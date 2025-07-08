from collections import UserString
from typing import Literal

from ..Enums import ParseMode

class TextFormat(UserString):
    def __init__(self, obj: object, parse_mode: ParseMode = ParseMode.HTML, screen_symbols: bool = True) -> None:
        self._parse_mode: ParseMode = parse_mode
        obj_text: str = str(obj)
        
        if screen_symbols:
            match self.parse_mode:
                case ParseMode.HTML:
                    screen_obj_text = obj_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    
                case _:
                    raise ValueError()
        else:
            screen_obj_text = obj_text
        
        super().__init__(screen_obj_text)
        
        
    def Bold(self) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<b>{self}</b>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Italic(self) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<i>{self}</i>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Underline(self) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<u>{self}</u>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Strikethrough(self) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<s>{self}</s>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Spoiler(self) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<tg-spoiler>{self}</tg-spoiler>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Link(self, href: str) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<a href={href}>{self}</a>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Pre(self) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<pre>{self}</pre>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Code(self, language: Literal['python']) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<code class="language-{language}">{self}</code>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
    
    def Blockquote(self, expandable: bool = False) -> 'TextFormat':
        match self.parse_mode:
            case ParseMode.HTML:
                text = f'<blockquote {'expandable' if expandable else ''}>{self}</blockquote>'
            
            case _:
                raise RuntimeError()
        return TextFormat(text, self.parse_mode, False)
            
    @property
    def parse_mode(self) -> ParseMode:
        return self._parse_mode
        
