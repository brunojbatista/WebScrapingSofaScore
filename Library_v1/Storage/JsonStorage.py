from filelock import Timeout, FileLock
from json.decoder import JSONDecodeError
import json
import re
import os
import importlib
from datetime import datetime, date, time
from pathlib import Path
from decimal import Decimal

PRIMITIVE_TYPES = (str, int, float, bool, type(None), list, dict, tuple)

# Tipos especiais embutidos do Python e como lidar com eles
SPECIAL_TYPES = {
    datetime: {
        "name": "datetime.datetime",
        "encoder": lambda obj: obj.isoformat(),
        "decoder": lambda val: datetime.fromisoformat(val)
    },
    date: {
        "name": "datetime.date",
        "encoder": lambda obj: obj.isoformat(),
        "decoder": lambda val: date.fromisoformat(val)
    },
    time: {
        "name": "datetime.time",
        "encoder": lambda obj: obj.isoformat(),
        "decoder": lambda val: time.fromisoformat(val)
    },
    set: {
        "name": "builtins.set",
        "encoder": lambda obj: list(obj),
        "decoder": lambda val: set(val)
    },
    frozenset: {
        "name": "builtins.frozenset",
        "encoder": lambda obj: list(obj),
        "decoder": lambda val: frozenset(val)
    },
    complex: {
        "name": "builtins.complex",
        "encoder": lambda obj: [obj.real, obj.imag],
        "decoder": lambda val: complex(val[0], val[1])
    },
    Decimal: {
        "name": "decimal.Decimal",
        "encoder": str,
        "decoder": lambda val: Decimal(val)
    },
    Path: {
        "name": "pathlib.Path",
        "encoder": str,
        "decoder": lambda val: Path(val)
    }
}

# Inverso para lookup por nome
SPECIAL_NAMES = {v["name"]: {"type": t, **v} for t, v in SPECIAL_TYPES.items()}


class JsonStorage:
    def __init__(self, filepath, timeout=60, indent=None):
        if re.search(r'\.json$', filepath) is None:
            filepath = f"{filepath}.json"

        self.filepath = filepath
        self.timeout = timeout
        self.indent = indent
        self.lock_path = f"{self.filepath}.lock"
        self.locker = FileLock(self.lock_path, timeout=1)

    def is_custom_object(self, obj):
        return not isinstance(obj, PRIMITIVE_TYPES)

    def encoder(self, obj):
        # Tipos especiais embutidos
        for typ, config in SPECIAL_TYPES.items():
            if isinstance(obj, typ):
                return {
                    "__type__": config["name"],
                    "__data__": config["encoder"](obj)
                }

        # Classes customizadas
        if self.is_custom_object(obj):
            return {
                "__type__": f"{obj.__class__.__module__}.{obj.__class__.__qualname__}",
                "__data__": obj.__dict__
            }

        raise TypeError(f"Objeto do tipo {type(obj)} não é serializável")

    def decoder(self, obj):
        if "__type__" in obj and "__data__" in obj:
            type_name = obj["__type__"]
            data = obj["__data__"]

            # Tipos especiais embutidos
            if type_name in SPECIAL_NAMES:
                return SPECIAL_NAMES[type_name]["decoder"](data)

            # Classes customizadas
            try:
                module_path, class_name = type_name.rsplit(".", 1)
                module = importlib.import_module(module_path)
                cls = getattr(module, class_name)
                instance = cls.__new__(cls)
                instance.__dict__.update(data)
                return instance
            except (ModuleNotFoundError, AttributeError) as e:
                raise ImportError(f"Erro ao importar classe {type_name}: {e}")
        return obj

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
        try:
            with open(self.filepath, encoding='utf-8') as file:
                return json.load(file, object_hook=self.decoder)
        except (FileNotFoundError, JSONDecodeError):
            return None

    def clean(self):
        try:
            with open(self.filepath, 'r+') as f:
                f.truncate(0)
            return True
        except FileNotFoundError:
            return False

    def delete(self):
        try:
            os.remove(self.filepath)
            return True
        except FileNotFoundError:
            return False
