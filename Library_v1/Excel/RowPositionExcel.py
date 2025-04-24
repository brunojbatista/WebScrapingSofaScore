import re

class RowPositionExcel():
    def __init__(self, start_row: int = 0, total_rows: int = 0) -> None:
        self.start_row = 0
        self.total_rows = 0
        # self.function_compare = None

        # self.reset_compare();
        self.set_start_row(start_row)
        self.set_total_rows(total_rows)
    
    def set_start_row(self, start_row: int):
        self.start_row = start_row

    def set_total_rows(self, total_rows: int):
        self.total_rows = total_rows

    def get_position(self, row: int) -> int:
        position = -1
        if not isinstance(row, int): raise TypeError("A linha precisa ser do tipo inteiro")
        offset = self.start_row - 1
        if not isinstance(row, int): raise TypeError("A linha precisa ser do tipo inteiro")
        if row > (self.total_rows + offset) or row < self.start_row:
            raise ValueError(f"A linha '{row}' é inválido")
        position = row - offset
        return position

    def get_range(self, ):
        final_row = self.total_rows + self.start_row
        return range(self.start_row, final_row)
