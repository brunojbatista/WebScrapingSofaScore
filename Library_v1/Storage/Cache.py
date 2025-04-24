from filelock import Timeout, FileLock
from filelock._error import Timeout
from Library_v1.Storage.FileStorage import FileStorage
import os
import time;

class Cache(FileStorage):
    def __init__(self, filepath, timeout=60):
        super().__init__(filepath, timeout)
        # self.filepath = filepath;
        # self.timeout = timeout;

    def write(self, data):
        self.lock();
        status = super().write(data)
        self.unlock();
        return status;

    def read(self, ):
        self.lock();
        content = super().read()
        self.unlock();
        return content;

    def clean(self, ):
        self.lock();
        status = super().clean()
        self.unlock();
        return status;

    def delete(self, ):
        self.lock();
        status = super().delete()
        self.unlock();
        return status;

    def join(self, data):
        self.lock();
        content = super().read()
        if content == None: content = "";
        content += data
        status = super().write(content)
        self.unlock();
        return status