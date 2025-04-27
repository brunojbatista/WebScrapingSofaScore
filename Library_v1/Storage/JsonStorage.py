from filelock import Timeout, FileLock
from json.decoder import JSONDecodeError
import json
import re
import os
from datetime import datetime, time

class JsonStorage:
    def __init__(self, filepath, timeout=60, indent=None):
        if re.search(r'\.json$', filepath) is None:
            filepath = f"{filepath}.json"

        self.filepath = filepath
        self.timeout = timeout
        self.indent = indent

        # Locker
        self.lock_path = f"{self.filepath}.lock"
        self.locker = FileLock(self.lock_path, timeout=1)

        # Lista de serializáveis
        self.serialize = []

        # Adicionando serializadores padrão
        self.add_serialize(
            'datetime', 
            datetime, 
            lambda obj: obj.isoformat(), 
            lambda obj: datetime.fromisoformat(obj['__value'])
        )

        self.add_serialize(
            'time', 
            time, 
            lambda obj: obj.isoformat(), 
            lambda obj: time.fromisoformat(obj['__value'])
        )

    def add_serialize(self, name: str, type_: type, encoder: callable, decoder: callable):
        """
        Adiciona uma nova regra de serialização e desserialização.
        """
        if not any(s['name'] == name for s in self.serialize):
            self.serialize.append({
                "name": name,
                "type": type_,
                "encoder": encoder,
                "decoder": decoder,
            })

    def get_seriable(self, key: str, value):
        for s in self.serialize:
            if key == 'name' and s[key] == value:
                return s
            elif key == 'type' and isinstance(value, s[key]):
                return s
        raise TypeError(f"Não foi possível encontrar o objeto serializável: '{key}'")

    def get_decoder(self, name: str) -> callable:
        return self.get_seriable('name', name)['decoder']

    def get_encoder(self, obj):
        return self.get_seriable('type', obj)

    def decoder(self, obj):
        """
        Função para desserializar objetos não padrão de JSON.
        """
        if not isinstance(obj, dict):
            return obj
        elif "__type" not in obj:
            return obj
        else:
            decoder = self.get_decoder(obj["__type"])
            return decoder(obj)

    def encoder(self, obj):
        seriable = self.get_encoder(obj)
        return {
            "__type": seriable['name'],
            "__value": seriable['encoder'](obj)
        }

    def lock(self):
        try:
            self.locker.acquire(timeout=self.timeout)
        except Timeout:
            raise TimeoutError(f"Expirou a espera pelo arquivo '{self.filepath}'")
        return True

    def unlock(self):
        self.locker.release()
        return True

    def write(self, data):
        try:
            serializable_data = json.dumps(data, ensure_ascii=False, default=self.encoder, indent=self.indent)
            with open(self.filepath, 'w', encoding='utf-8') as file:
                file.write(serializable_data)
            return True
        except FileNotFoundError:
            return False

    def read(self):
        """
        Lê os dados do arquivo e os desserializa.
        """
        try:
            with open(self.filepath, encoding='utf-8') as file:
                return json.load(file, object_hook=self.decoder)
        except FileNotFoundError:
            return None
        except JSONDecodeError:
            return None

    def clean(self):
        """
        Limpa o conteúdo do arquivo JSON.
        """
        try:
            with open(self.filepath, 'r+') as f:
                f.truncate(0)
            return True
        except FileNotFoundError:
            return False

    def delete(self):
        """
        Remove o arquivo JSON.
        """
        try:
            os.remove(self.filepath)
            return True
        except FileNotFoundError:
            return False
