import re

class ColumnPositionExcel():
    def __init__(self, columns: list = []) -> None:
        self.columns = columns
        self.total_columns = len(columns)
        self.function_compare = None

        self.reset_compare();
        self.set_columns(columns)
    
    def set_columns(self, columns: list):
        self.columns = columns
        self.total_columns = len(columns)

    def reset_compare(self, ):
        self.set_compare(lambda regex, value: not re.search(regex, value, flags=re.I) is None)

    def set_compare(self, function):
        self.function_compare = function

    # def set_column_letters(self, ):
    #     for column_int in range(1, self.total_columns+1):
    #         start_index = 1   #  it can start either at 0 or at 1
    #         letter = ''
    #         while column_int > 25 + start_index:   
    #             letter += chr(65 + int((column_int-start_index)/26) - 1)
    #             column_int = column_int - (int((column_int-start_index)/26))*26
    #         letter += chr(65 - start_index + (int(column_int)))
    #         self.columns_letters.append(letter)

    def get_position(self, column: str|int) -> int:
        position = -1
        if isinstance(column, int):
            if column > self.total_columns or column <= 0:
                raise ValueError(f"A coluna '{column}' não foi encontrada")
            position = column
        elif isinstance(column, str):
            for index, col in enumerate(self.columns):
                if not self.function_compare(column, col): continue;
                position = index + 1
                break;
            if position < 0: raise ValueError(f"A coluna '{column}' não foi encontrada")
        else:
            raise ValueError(f"O tipo da coluna de busca é inválido")
        return position;

    def get_name(self, column: str|int) -> str:
        return self.columns[self.get_position(column) - 1]

    def get_range(self, ):
        return range(1, self.total_columns+1)
