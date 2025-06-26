from typing import overload, Generator, AsyncIterator, AsyncContextManager
from contextlib import asynccontextmanager
import asyncio

from .. import DefaultTypes
from ...Enums import Action


class ChatAction:
    def __init__(self, bot, chat: DefaultTypes.Chat):
        from ...Bot import Bot
        self.bot: Bot = bot
        self.chat: DefaultTypes.Chat = chat
    
    async def _KeepSendingAction(self, action: Action, stop_event: asyncio.Event):
        while not stop_event.is_set():
            try:
                await self.bot.methods.SendChatAction(self.chat.id, action)
                
            except Exception as e:
                print(f"Error sending chat action: {e}")
                
            finally:
                await asyncio.wait_for(stop_event.wait(), timeout=5)
    
    @asynccontextmanager
    async def _Action(self, action: Action) -> AsyncIterator[None]:
        try:
            stop_event = asyncio.Event()
            task = asyncio.create_task(self._KeepSendingAction(action, stop_event))
            yield
        finally:
            stop_event.set()
            await task

    def Typing(self) -> AsyncContextManager[None]:
        return self._Action(Action.TYPING)
    
    def UploadPhoto(self) -> AsyncContextManager[None]:
        return self._Action(Action.UPLOAD_PHOTO)
    
    def RecordVideo(self) -> AsyncContextManager[None]:
        return self._Action(Action.RECORD_VIDEO)
    
    def UploadVideo(self) -> AsyncContextManager[None]:
        return self._Action(Action.UPLOAD_VIDEO)
    
    def RecordVoice(self) -> AsyncContextManager[None]:
        return self._Action(Action.RECORD_VOICE)
    
    def UploadVoice(self) -> AsyncContextManager[None]:
        return self._Action(Action.UPLOAD_VOICE)
    
    def UploadDocument(self) -> AsyncContextManager[None]:
        return self._Action(Action.UPLOAD_DOCUMENT)
    
    def ChooseSticker(self) -> AsyncContextManager[None]:
        return self._Action(Action.CHOOSE_STICKER)
    
    def FindLocation(self) -> AsyncContextManager[None]:
        return self._Action(Action.FIND_LOCATION)
    
    def RecordVideoNote(self) -> AsyncContextManager[None]:
        return self._Action(Action.RECORD_VIDEO_NOTE)
    
    def UploadVideoNote(self) -> AsyncContextManager[None]:
        return self._Action(Action.UPLOAD_VIDEO_NOTE)
