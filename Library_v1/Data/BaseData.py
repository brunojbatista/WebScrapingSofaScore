import re

class BaseData():
    def __init__(self, **parameters) -> None:
        for key, value in parameters.items(): setattr(self, key, value)

    def __getattr__(self, method_name):
        # Quando um método que não existe for chamado, esse método será ativado
        if re.search(r"^set_all*$", method_name, flags=re.I):
            # Método especial para `set_all` que aceita um dicionário de propriedades
            def set_all(values):
                for key, value in values.items():
                    # Verifica se a propriedade existe na classe antes de atribuir
                    if hasattr(self, key):
                        setattr(self, key, value)
                    else:
                        raise AttributeError(f"Propriedade '{key}' não existe na classe.")
            # Retorna o método set_all
            return set_all
        elif re.search(r"get_all", method_name, flags=re.I):
            # Método especial para `get_all` que retorna um dicionário com as propriedades e seus valores
            def get_all():
                # Vamos criar um dicionário com todas as propriedades e seus valores
                values = {key: value for key, value in self.__dict__.items()}
                return values
            # Retorna o método get_all
            return get_all
        elif method_name.startswith('set_'):
            property_name = method_name[4:]  # Remove o "set_"
            # Criamos dinamicamente o método "setter"
            def setter_method(value):
                # Verifica se a propriedade existe
                if hasattr(self, property_name):
                    # aplicar a regra de negócio para cada propriedade
                    setattr(self, property_name, value)
                else:
                    raise AttributeError(f"Propriedade '{property_name}' não existe na classe.")
            # Retornamos o método criado dinamicamente
            return setter_method
        elif method_name == 'set':
            # Criamos dinamicamente o método "setter"
            def setter_method(property_name, value):
                # Verifica se a propriedade existe
                if hasattr(self, property_name):
                    # aplicar a regra de negócio para cada propriedade
                    setattr(self, property_name, value)
                else:
                    raise AttributeError(f"Propriedade '{property_name}' não existe na classe.")
            # Retornamos o método criado dinamicamente
            return setter_method
        elif method_name.startswith('get_'):
            property_name = method_name[4:]  # Remove o "get_"
            # Verifica se a propriedade existe
            def getter_method():
                if hasattr(self, property_name):
                    return getattr(self, property_name)
                else:
                    raise AttributeError(f"Propriedade '{property_name}' não existe na classe.")
            return getter_method
        elif method_name == 'get':
            def getter_method(property_name):
                if hasattr(self, property_name):
                    return getattr(self, property_name)
                else:
                    raise AttributeError(f"Propriedade '{property_name}' não existe na classe.")
            return getter_method
        elif method_name.startswith('del_'):
            property_name = method_name[4:]  # Remove o "del_"
            def deleter_method():
                if hasattr(self, property_name):
                    delattr(self, property_name)
                else:
                    raise AttributeError(f"Propriedade '{property_name}' não existe na classe.")
            return deleter_method
        elif method_name == 'delete' or method_name == 'del':
            def deleter_method(property_name):
                if hasattr(self, property_name):
                    delattr(self, property_name)
                else:
                    raise AttributeError(f"Propriedade '{property_name}' não existe na classe.")
            return deleter_method
        else:
            raise AttributeError(f"Método '{method_name}' não encontrado na classe.")
        
    def update(self, obj) -> bool:
        not NotImplementedError