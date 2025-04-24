from abc import ABC, abstractmethod

class DriverInterface(ABC):

    @abstractmethod
    def set_download_path(self, download_path: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_download_path(self, ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_download_relativepath(self, ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def find_download_file(self, searched_name, path = None):
        raise NotImplementedError

    @abstractmethod
    def open(self):
        raise NotImplementedError

    @abstractmethod
    def is_open(self, ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def set_wait(self, timeout = 1, ref = None):
        raise NotImplementedError

    @abstractmethod
    def set_condition(self, ec_function):
        raise NotImplementedError
    
    @abstractmethod
    def refresh(self, ):
        raise NotImplementedError

    @abstractmethod
    def get_url(self, url: str):
        raise NotImplementedError
    
    @abstractmethod
    def clear_storage(self, ):
        raise NotImplementedError
    
    @abstractmethod
    def clear_cookies(self, ):
        raise NotImplementedError
    
    @abstractmethod
    def garbage_collection(self, ):
        raise NotImplementedError
    
    @abstractmethod
    def optimize_memory(self, ):
        raise NotImplementedError

    @abstractmethod
    def lock(self, timeout : int = 30):
        raise NotImplementedError

    @abstractmethod
    def unlock(self, ):
        raise NotImplementedError

    @abstractmethod
    def get_session_id(self):
        raise NotImplementedError

    @abstractmethod
    def get_title(self):
        raise NotImplementedError

    @abstractmethod
    def get_current_url(self):
        raise NotImplementedError
    
    @abstractmethod
    def get(self, ):
        raise NotImplementedError
    
    @abstractmethod
    def set_download_path(self, ):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def execute_script(self, script: str):
        raise NotImplementedError
    
    @abstractmethod
    def execute_async_script(self, script: str):
        raise NotImplementedError

    @abstractmethod
    def get_windows(self, ) -> list:
        raise NotImplementedError

    @abstractmethod
    def get_current_window(self, ) -> str:
        raise NotImplementedError

    @abstractmethod
    def switch_window(self, handle: str):
        raise NotImplementedError
    
    @abstractmethod
    def new_window(self, ) -> str:
        raise NotImplementedError

    # @abstractmethod
    # def write(self, data) -> bool:
    #     raise NotImplementedError

    # @abstractmethod
    # def read(self):
    #     raise NotImplementedError

    # @abstractmethod
    # def clear(self) -> bool:
    #     raise NotImplementedError

    # @abstractmethod
    # def delete(self) -> bool:
    #     raise NotImplementedError