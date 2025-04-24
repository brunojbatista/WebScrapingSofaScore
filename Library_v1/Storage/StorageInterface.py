from abc import ABC, abstractmethod

class StorageInterface(ABC):

    @abstractmethod
    def lock(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def unlock(self) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def write(self, data) -> bool:
        raise NotImplementedError

    @abstractmethod
    def read(self):
        raise NotImplementedError

    @abstractmethod
    def clean(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> bool:
        raise NotImplementedError