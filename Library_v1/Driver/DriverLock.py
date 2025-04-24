from filelock import Timeout, FileLock

from Library_v1.Utils.file import (
    get_relative_full_path,
    separator,
)

class DriverLock():

    def __init__(self, ) -> None:
        infopath = get_relative_full_path("Library/Driver/Lockers", True)
        self.filepath = separator(f"{infopath['fullpath']}/DriverLock.lock")
        self.locker = FileLock(self.filepath);

    def get_filepath(self, ):
        return self.filepath;

    def lock(self, timeout : int = 60):
        try:
            self.locker.acquire(timeout=timeout);
        except Timeout:
            raise TimeoutError(f"Falhou a aquisição do driver")
        return self;

    def unlock(self):
        self.locker.release();
        return self

    
