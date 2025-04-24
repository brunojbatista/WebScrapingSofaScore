import json
import re
import os
from Library_v1.Storage.StorageInterface import StorageInterface

class MemoryStorage(StorageInterface):
    def __init__(self):
        self.data = {}

    def lock(self):
        return True;
    
    def unlock(self):
        return True;

    def write(self, data):
        self.data = data;
        return True;

    def read(self):
        return self.data;

    def clean(self):
        self.data = {};
        return True;

    def delete(self):
        return self.clear();