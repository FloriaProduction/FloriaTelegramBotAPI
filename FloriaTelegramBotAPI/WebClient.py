import httpx
from typing import Any, Optional
import json

from .Config import Config
from . import Utils, Protocols


class WebClient:
    def __init__(self, token: str, config: Config):
        self.__token = token
        self._config: Config = config
        
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
    
    async def GetUpdates(self, update_offset: int) -> list[dict[str, Any]]:
        return (await self.RequestGet(
            'getUpdates', 
            {
                'offset': update_offset + 1
            }
        )).get('result', [])
    
    async def MakeRequest(
        self, 
        method: Protocols.Functions.CommonCallableAsync, 
        command: str,
        **kwargs: Any
    ) -> dict[str, Any]:
        current_attempt_count = 0
        while current_attempt_count < self.config.retry_count:
            try:
                response: httpx.Response = await method(
                    url=f'https://api.telegram.org/bot{self.__token}/{command}',
                    **kwargs
                )
                data: dict[str, Any] = response.json()
                if not response.is_success:
                    raise Exception(f'\n\tCode: {data.get('error_code')}\n\tDescription: {data.get('description')}\n\tCommand: {command}\n\tRequest: \n{ json.dumps(json.loads(response.request.content.decode()), ensure_ascii=False, indent=4) }')
                
                return data
            
            finally:
                current_attempt_count += 1
        
        raise httpx.RequestError(f'Failed to complete request after {self.config.retry_count} attempts')
        
    async def RequestGet(
        self, 
        command: str, 
        data: Optional[Any] = None
    ) -> dict[str, Any]:
        return await self.MakeRequest(
            self._client.get, 
            command,
            
            params=Utils.ConvertToJson(data or {})
        )
    
    async def RequestPost(
        self, 
        command: str, 
        data: Any,
    ) -> dict[str, Any]:
        return await self.MakeRequest(
            self._client.post, 
            command,
            
            json=Utils.ConvertToJson(data or {}),
        )
    
    async def RequestPostData(
        self,
        command: str,
        data: Any,
        files: Any = None
    ) -> dict[str, Any]:
        return await self.MakeRequest(
            self._client.post,
            command,
            
            data=Utils.ConvertToJson(data or {}),
            files=files
        )
    
    @property
    def config(self) -> Config:
        return self._config