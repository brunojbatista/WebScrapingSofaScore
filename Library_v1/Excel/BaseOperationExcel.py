from Library_v1.Excel.StorageDataExcel import StorageDataExcel

class BaseOperationExcel(StorageDataExcel):
    def __init__(self, columns: list = [], rows: list = []) -> None:
        StorageDataExcel.__init__(self, columns, rows)

    def check_position_column(self, position_column: int) -> bool:
        if not isinstance(position_column, int): raise TypeError("A posição da coluna deve ser um inteiro")
        return position_column > 0 and position_column <= self.get_total_columns()
    
    def check_position_row(self, position_row: int) -> bool:
        if not isinstance(position_row, int): raise TypeError("A posição da linha deve ser um inteiro")
        return position_row > 0 and position_row <= self.get_total_rows()
    
    ###########################################################################
    # OPERAÇÕES BASE

    def swap_value(self, position_1: tuple, position_2: tuple): # ok
        (pos_row_1, pos_col_1) = position_1
        (pos_row_2, pos_col_2) = position_2
        if not self.check_position_row(pos_row_1):      raise ValueError("A posição da linha 1 está fora do permitido")
        if not self.check_position_column(pos_col_1):   raise ValueError("A posição da coluna 1 está fora do permitido")
        if not self.check_position_row(pos_row_2):      raise ValueError("A posição da linha 2 está fora do permitido")
        if not self.check_position_column(pos_col_2):   raise ValueError("A posição da coluna 2 está fora do permitido")
        rows = self.get_rows()
        value_1 = rows[pos_row_1 - 1][pos_col_1 - 1]
        value_2 = rows[pos_row_2 - 1][pos_col_2 - 1]
        rows[pos_row_1 - 1][pos_col_1 - 1] = value_2
        rows[pos_row_2 - 1][pos_col_2 - 1] = value_1
        self.set_rows(rows)
        return True

    def read_value(self, position: tuple): # ok
        (pos_row, pos_col) = position
        if not self.check_position_row(pos_row):      raise ValueError("A posição da linha está fora do permitido")
        if not self.check_position_column(pos_col):   raise ValueError("A posição da coluna está fora do permitido")
        rows = self.get_rows()
        value = rows[pos_row - 1][pos_col - 1]
        return value
    
    def write_value(self, position: tuple, value: any) -> bool: # ok
        (pos_row, pos_col) = position
        if not self.check_position_row(pos_row):      raise ValueError("A posição da linha está fora do permitido")
        if not self.check_position_column(pos_col):   raise ValueError("A posição da coluna está fora do permitido")
        rows = self.get_rows()
        rows[pos_row - 1][pos_col - 1] = value
        self.set_rows(rows)
        return True
    
    def add_row(self, position_row_ref: int, position: str = 'after') -> int: # ok
        if not self.check_position_row(position_row_ref): raise ValueError("A posição da linha de referência está fora do permitido")
        rows = self.get_rows()
        new_row = [None] * self.get_total_columns()
        new_position = position_row_ref + 1
        if position == 'after':
            rows = [*rows[0:position_row_ref], new_row, *rows[position_row_ref:]]
        elif position == 'before':
            new_position = position_row_ref
            rows = [*rows[0:(position_row_ref-1)], new_row, *rows[(position_row_ref-1):]]
        self.set_rows(rows)
        return new_position
    
    def delete_row(self, position_row: int) -> list: # ok
        if not self.check_position_row(position_row): raise ValueError("A posição da linha está fora do permitido")
        row = []
        before_position = position_row - 1
        rows = self.get_rows()
        row = rows[position_row - 1]
        rows = [*rows[0:before_position], *rows[(before_position+1):]]
        self.set_rows(rows)
        return row;
    
    def add_column(self, column_name: str, position_column_ref: int, position: str = 'after') -> int:
        if not self.check_position_column(position_column_ref): raise ValueError("A posição da coluna de referência está fora do permitido")
        rows = self.get_rows()
        columns = self.get_columns()
        if position == 'after':
            new_position = position_column_ref + 1
        elif position == 'before':
            new_position = position_column_ref
        before_position = new_position - 1
        for index_row, row in enumerate(rows):
            row = row[:before_position] + [None] + row[before_position:]
            rows[index_row] = row
        columns = columns[:before_position] + [column_name] + columns[before_position:]
        self.set_rows(rows)
        self.set_columns(columns)
        return new_position
    
    def delete_column(self, position_column: int) -> list: # ok
        if not self.check_position_column(position_column): raise ValueError("A posição da coluna de referência está fora do permitido")
        extracted_columns = []
        before_position = position_column - 1
        rows = self.get_rows()
        columns = self.get_columns()
        for index_row, row in enumerate(rows):
            extracted_columns.append(row[position_column-1])
            row = row[:before_position] + row[(before_position+1):]
            rows[index_row] = row
        columns = columns[:before_position] + columns[(before_position+1):]
        self.set_rows(rows)
        self.set_columns(columns)
        return extracted_columns
    
    # def order_column(self, position_column: int, reverse: bool = False) -> bool: # ok
    #     if not self.check_position_column(position_column): raise ValueError("A posição da coluna de referência está fora do permitido")
    #     rows = self.get_rows()
    #     rows = sorted(rows, key=lambda d: d[position_column-1], reverse=reverse)
    #     self.set_rows(rows)
    #     return True
    
    def order_columns(self, position_columns: list, reverse: bool = False) -> bool: # ok
        for col_pos in position_columns: 
            if not self.check_position_column(col_pos): raise ValueError("A posição da coluna de referência está fora do permitido")
        rows = self.get_rows()
        rows.sort(key=lambda d: [d[pos-1] for pos in position_columns], reverse=reverse)
        self.set_rows(rows)
        return True
    
    ###########################################################################
    # OPERAÇÕES AVANÇADAS

    def read_row(self, position_row: int) -> list: # ok
        row = []
        for position_col in range(1, self.get_total_columns() + 1):
            row.append(self.read_value((position_row, position_col)))
        return row;

    def write_row(self, position_row: int, values: list) -> bool: # ok
        total_values = len(values)
        if total_values < self.get_total_columns():
            values += [None] * (self.get_total_columns() - total_values)
        for position_col in range(1, self.get_total_columns() + 1):
            self.write_value((position_row, position_col), values[position_col-1])
        return True;

    def read_column(self, position_column: int) -> list: # ok
        column = []
        for position_row in range(1, self.get_total_rows() + 1):
            column.append(self.read_value((position_row, position_column)))
        return column

    def write_column(self, position_column: int, values: list) -> bool: # ok
        total_values = len(values)
        if total_values < self.get_total_rows():
            values += [None] * (self.get_total_rows() - total_values)
        for position_row in range(1, self.get_total_rows() + 1):
            self.write_value((position_row, position_column), values[position_row-1])
        return True;
    
    def swap_row(self, position_row_1: int, position_row_2: int): # ok
        for position_col in range(1, self.get_total_columns() + 1):
            self.swap_value((position_row_1, position_col), (position_row_2, position_col))

    def swap_column(self, position_column_1: int, position_column_2: int): # ok
        for position_row in range(1, self.get_total_rows() + 1):
            self.swap_value((position_row, position_column_1), (position_row, position_column_2))

    def group_columns(self, position_columns: list) -> list: # ok
        groups = []
        columns = []
        total_values = 0
        total_position = len(position_columns)
        for pos in position_columns:
            cols = self.read_column(pos)
            total_values = len(cols)
            columns.append(cols)
        for index_value in range(0, total_values):
            group = []
            for index_position in range(0, total_position):
                group.append(columns[index_position][index_value])
            groups.append(group)
        return groups;

    def append_column(self, column_name: str) -> int:
        last_column_position = self.get_total_columns()
        new_last_column_position = self.add_column(column_name, last_column_position, 'after')
        return new_last_column_position;
        

