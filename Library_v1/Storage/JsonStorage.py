from filelock import Timeout, FileLock
from filelock._error import Timeout
from json.decoder import JSONDecodeError
import json
import re
import os
from Library_v1.Storage.StorageInterface import StorageInterface

def encoder(obj):
    from datetime import datetime

    if isinstance(obj, datetime):
        return {
            "__type": "datetime",
            "__value": str(obj)
        }
    raise TypeError(f"Não foi possível serializar o objeto '{obj}'")

def decoder(obj):
    if not(isinstance(obj, dict)):
        return obj;
    elif "__type" not in obj:
        return obj;
    else:
        from datetime import datetime
        
        if obj["__type"] == "datetime":
            return datetime.fromisoformat(obj['__value'])

    raise TypeError(f"Não foi possível desserializar o objeto '{obj}'")
    


class JsonStorage(StorageInterface):
    def __init__(self, filepath, timeout=60, indent=None):
        if re.search(r'\.json$', filepath) == None:
            filepath = f"{filepath}.json";
        
        self.filepath = filepath;
        self.timeout = timeout;
        self.indent = indent;

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
        return True;

    def write(self, data):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                file.write(json.dumps(data, ensure_ascii=False, default=encoder, indent=self.indent))
                file.close()
            return True;
        except FileNotFoundError:
            return False;

    def read(self):
        try:
            try:
                with open(self.filepath, encoding='utf-8') as file:
                    content = json.loads(file.read(), object_hook=decoder);
                    file.close()
            except JSONDecodeError:
                return None
            return content;
        except FileNotFoundError:
            return None

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