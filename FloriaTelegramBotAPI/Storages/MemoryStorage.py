from typing import Generic, Optional, Iterator, Iterable
from ..Abc.Storage import Storage, TStorageValue
from ..Types import KEY_TYPES


class MemoryStorage(Storage[TStorageValue], Generic[TStorageValue]):
    def __init__(self):
        super().__init__()
        
        self._memory: dict[KEY_TYPES, TStorageValue] = {}
    
    def Get(self, key: KEY_TYPES, default: Optional[TStorageValue] = None) -> Optional[TStorageValue]:
        return self._memory.get(key, default)
    
    def Set(self, key: KEY_TYPES, value: TStorageValue) -> KEY_TYPES:
        self._memory[key] = value
        return key
    
    def Pop(self, key: KEY_TYPES, default: Optional[TStorageValue] = None) -> Optional[TStorageValue]:
        return self._memory.pop(key, default)
    
    def Has(self, key: KEY_TYPES) -> bool:
        return key in self._memory
    
    def Keys(self) -> Iterable[KEY_TYPES]:
        return [*self._memory.keys()]
    
    def Values(self) -> Iterable[TStorageValue]:
        return [*self._memory.values()]
    
    def Items(self) -> Iterable[tuple[KEY_TYPES, TStorageValue]]:
        return [*self._memory.items()]

    def __len__(self) -> int:
        return len(self._memory)