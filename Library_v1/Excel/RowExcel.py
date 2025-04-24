import re

class RowExcel():
    def __init__(self, columns: list, values: list) -> None:
        self.columns = columns
        self.values = values
        self.value = None;
        self.regex_value = None
    
    def regex(self, regex_col):
        print(f"regex_col: {regex_col}")
        target_indexes = []
        self.value = None;
        for index, col in enumerate(self.columns):
            if re.search(regex_col, col, flags=re.I):
                target_indexes.append(index)
                break;
        if len(target_indexes) > 0: self.value = self.values[target_indexes[0]]
        else: raise ValueError(f"Não existe a coluna buscada '{regex_col}'")
        return self;

    def equal(self, ref_col):
        target_indexes = []
        self.value = None;
        for index, col in enumerate(self.columns):
            if ref_col == col:
                target_indexes.append(index)
                break;
        if len(target_indexes) > 0: self.value = self.values[target_indexes[0]]
        else: raise ValueError(f"Não existe a coluna buscada '{ref_col}'")
        return self;

    def get(self, ):
        print(f"self.value: {self.value}")
        if re.search(r"^(\s*|None)$", str(self.value), flags=re.I): return None;
        return self.value

    