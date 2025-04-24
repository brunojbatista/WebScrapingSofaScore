
"""
    Ordernar uma lista de objetos com referência a uma chave desse objeto
"""
def order_list_of_dict(arr: list, key: str):
    return sorted(arr, key=lambda d: d[key])