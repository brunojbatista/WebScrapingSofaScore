from filelock import Timeout, FileLock
from filelock._error import Timeout
from Library_v1.Storage.StorageInterface import StorageInterface
import os
import time;

class FileStorage(StorageInterface):
    def __init__(self, filepath, timeout=60):
        self.filepath = filepath;
        self.timeout = timeout;

        # Locker
        self.lock_path = "{}.lock".format(self.filepath);
        self.locker = FileLock(self.lock_path, timeout=1);

    def lock(self):
        try:
            self.locker.acquire(timeout=self.timeout);
        except Timeout:
            raise TimeoutError(f"Expirou a espera pelo arquivo '{self.filepath}'")
        return True;
    
    def unlock(self):
        self.locker.release();
        return self;

    def write(self, data):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                file.write(data)
                file.close()
            return True;
        except FileNotFoundError:
            return False;

    def read(self):
        try:
            with open(self.filepath, encoding='utf-8') as file:
                content = file.read();
                file.close()
            return content;
        except FileNotFoundError:
            return None;

    def clean(self):
        try:
            with open(self.filepath, 'r+') as f:
                f.truncate(0)
            return True;
        except FileNotFoundError:
            return False;

    def delete(self):
        try:
            os.remove(self.filepath)
            return True;
        except FileNotFoundError:
            return False;