from Library_v1.Excel.BaseOperationExcel import BaseOperationExcel
from Library_v1.Excel.ReadingExcel import ReadingExcel
from Library_v1.Excel.ColumnPositionExcel import ColumnPositionExcel
from Library_v1.Excel.RowPositionExcel import RowPositionExcel
from Library_v1.Excel.SaveExcel import SaveExcel
from Library_v1.Excel.RowExcel import RowExcel

class StructExcel():
    def __init__(self) -> None:
        self.operation          = BaseOperationExcel()
        self.manipulate_columns = ColumnPositionExcel()
        self.manipulate_rows    = RowPositionExcel()
        self.columns_search     = []
        self.columns_name       = []
        self.columns_position   = []
        self.rows_search        = []
        self.rows_number        = []
        self.rows_position      = []
        self.start_row_pos      = 1;
        self.compare_function   = None;

    def read_excel(self, filepath: str, tab_name: str|int = 1, start_column_pos: int = 1, start_row_pos: int = None):
        # ------------------------------------------------------
        # Abertura do excel e leitura dos dados
        reader = ReadingExcel(filepath)
        reader.set_sheet(tab_name).set_start_column(start_column_pos)
        if not start_row_pos is None: 
            reader.set_start_row(start_row_pos)
            self.start_row_pos = reader.get_row_position()

        # ------------------------------------------------------
        # Atualização dos parametros da estrutura do excel
        self.operation.set_columns(reader.get_columns())
        self.operation.set_rows(reader.get_rows())
        self.manipulate_columns.set_columns(self.operation.get_columns())
        self.manipulate_rows.set_start_row(reader.get_row_position())
        self.manipulate_rows.set_total_rows(self.operation.get_total_rows())
        self.manipulate_columns.reset_compare()
        self.reset()

        del reader
        return self;

    def load_data(self, columns: list, rows: list, start_row_pos: int = 1):
        # ------------------------------------------------------
        # Atualização dos parametros da estrutura do excel
        self.operation.set_columns(columns)
        self.operation.set_rows(rows)
        self.manipulate_columns.set_columns(self.operation.get_columns())
        self.manipulate_rows.set_start_row(start_row_pos)
        self.start_row_pos = start_row_pos
        self.manipulate_rows.set_total_rows(self.operation.get_total_rows())
        self.manipulate_columns.reset_compare()
        self.reset()

    def import_params(self, params: dict):
        for param in params: setattr(self, param, params[param])

    def export_params(self, ):
        from copy import copy
        params = {}
        for attribute, value in self.__dict__.items():
            params[attribute] = copy(value)
        return params

    def update_manipulate_positions(self, ):
        self.manipulate_columns.set_columns(self.operation.get_columns())
        self.manipulate_rows.set_total_rows(self.operation.get_total_rows())

    def read_columns_position(self, *columns_parms) -> list:
        return [self.manipulate_columns.get_position(x) for x in list(columns_parms)]

    def set_compare_column(self, compare_function):
        self.compare_function = compare_function
        self.manipulate_columns.set_compare(compare_function)

    def get_columns(self, ) -> list:
        return self.operation.get_columns()
    
    def get_rows(self, ) -> list:
        return self.operation.get_rows()
    
    def get_total_columns(self, ) -> int:
        return self.operation.get_total_columns();
    
    def get_total_rows(self, ) -> int:
        return self.operation.get_total_rows();

    def col(self, *columns):
        self.columns_search = list(columns)
        self.columns_position = []
        self.columns_name = []
        for col in self.columns_search: 
            column_position = self.manipulate_columns.get_position(col)
            self.columns_position.append(column_position)
            col_name = self.manipulate_columns.get_name(column_position)
            # print(f"col_name: {col_name}")
            self.columns_name.append(self.manipulate_columns.get_name(column_position))
        # print(f"self.columns_position: {self.columns_position}")
        # print(f"self.columns_name: {self.columns_name}")
        return self;

    def row(self, *rows):
        self.rows_search = list(rows)
        self.rows_position = []
        self.rows_number = []
        for row in self.rows_search: 
            row_position = self.manipulate_rows.get_position(row)
            self.rows_position.append(row_position)
            self.rows_number.append(row_position)
        # print(f"self.rows_position: {self.rows_position}")
        return self;

    def reset(self, ):
        self.columns_position = []
        self.rows_position = []
        return self;

    def check_rows(self, min_rows: int = 1):
        if len(self.rows_position) < min_rows: raise ValueError(f"É preciso ter no mínimo {min_rows} linha(s)")

    def check_columns(self, min_cols: int = 1):
        if len(self.columns_position) < min_cols: raise ValueError(f"É preciso ter no mínimo {min_cols} coluna(s)")

    ##########################################################################
    ## 

    def get(self, ): # ok
        self.check_rows()
        self.check_columns()
        row_position    = self.rows_position[0]
        column_position = self.columns_position[0]
        return self.operation.read_value((row_position, column_position))

    def get_row(self, ): # ok
        self.check_rows()
        rows = []
        for row_position in self.rows_position:
            rows.append(self.operation.read_row(row_position))
        return rows;

    def get_column(self, ): # ok
        self.check_columns()
        columns = []
        for column_position in self.columns_position:
            columns.append(self.operation.read_column(column_position))
        return columns;

    def order_columns(self, reverse: bool = False) -> bool: # ok
        self.check_columns()
        return self.operation.order_columns(self.columns_position, reverse)
    
    def group_columns(self, ): # ok
        self.check_columns()
        position_columns = self.columns_position
        return self.operation.group_columns(position_columns)

    def delete_column(self, ): # ok
        self.check_columns()
        column_position = self.columns_position[0]
        columns = self.operation.delete_column(column_position)
        self.update_manipulate_positions()
        return self;
    
    def add_column_after(self, *columns_name): # ok
        self.check_columns()
        columns = list(columns_name)
        for col_name in columns[::-1]:
            self.operation.add_column(col_name, self.columns_position[0], 'after')
        self.update_manipulate_positions()
        return self;

    def add_column_before(self, *columns_name): # ok
        self.check_columns()
        columns = list(columns_name)
        for col_name in columns[::-1]:
            self.operation.add_column(col_name, self.columns_position[0], 'before')
        self.update_manipulate_positions()
        return self;

    def append_column(self, *columns_name): # ok
        columns = list(columns_name)
        for col_name in columns:
            self.operation.append_column(col_name)
        self.update_manipulate_positions()
        return self;

    def map_column(self, map_function, *columns_parms): # ok
        self.check_columns()
        column_position = self.columns_position[0];
        columns_parms_position = self.read_columns_position(*columns_parms)
        grouped = self.operation.group_columns(columns_parms_position)
        if len(grouped) <= 0: grouped = self.operation.group_columns([column_position])
        new_column = []
        for group in grouped:
            response = map_function(*group)
            new_column.append(response)
        self.operation.write_column(column_position, new_column)
        return self;
    
    def filter_rows(self, filter_function, *columns_parms): # ok
        columns_parms_position = self.read_columns_position(*columns_parms)
        if len(columns_parms_position) <= 0: raise ValueError("Para o filtro de linhas é preciso definir ao menos uma coluna")
        grouped = self.operation.group_columns(columns_parms_position)
        filtered_rows = []
        grouped_index = 0
        for row in self.manipulate_rows.get_range():
            row_pos = self.manipulate_rows.get_position(row)
            response = bool(filter_function(*grouped[grouped_index]))
            grouped_index += 1
            if not response: continue;
            filtered_rows.append(self.operation.read_row(row_pos))
        self.operation.set_rows(filtered_rows)
        self.update_manipulate_positions()
        return self;

    def foreach_rows(self, foreach_function, *columns_parms): # ok
        columns_parms_position = self.read_columns_position(*columns_parms)
        if len(columns_parms_position) <= 0: raise ValueError("Para rodar as linhas é preciso definir ao menos uma coluna")
        grouped = self.operation.group_columns(columns_parms_position)
        for group in grouped:
            foreach_function(*group)
        return self;

    def foreach_row(self, foreach_function): # ok
        columns = self.get_columns()
        columns_parms_position = self.read_columns_position(*columns)
        if len(columns_parms_position) <= 0: raise ValueError("Para rodar as linhas é preciso definir ao menos uma coluna")
        for row in self.manipulate_rows.get_range():
            row_pos = self.manipulate_rows.get_position(row)
            foreach_function(RowExcel(columns, self.operation.read_row(row_pos)))
        return self;

    def delete_columns(self, ): # ok
        self.check_columns()
        while True:
            if len(self.columns_name) <= 0: break;
            col_name = self.columns_name.pop(0)
            column_position = self.manipulate_columns.get_position(col_name)
            columns = self.operation.delete_column(column_position)
            self.update_manipulate_positions()
        return self;

    def search_rows_position_by_column(self, value) -> list:
        self.check_columns()
        rows_position = []
        column_position = self.columns_position[0];
        for row in self.manipulate_rows.get_range():
            row_pos = self.manipulate_rows.get_position(row)
            reading_value = self.operation.read_value((row_pos, column_position))
            print(f"reading_value: {reading_value}")
            if reading_value != value: continue;
            rows_position.append(row_pos)
        return rows_position;

    def search_values_by_column(self, search_function, *columns_parms) -> list: # ok
        values = []
        self.check_columns()
        column_position = self.columns_position[0];
        columns_parms_position = self.read_columns_position(*columns_parms)
        grouped = self.operation.group_columns(columns_parms_position)
        if len(grouped) <= 0: 
            columns_parms_position = [column_position]
            grouped = self.operation.group_columns(columns_parms_position)
        grouped_index = 0
        for row in self.manipulate_rows.get_range():
            row_pos = self.manipulate_rows.get_position(row)
            params = grouped[grouped_index]
            grouped_index += 1
            if not search_function(*params): continue;
            row = self.operation.read_row(row_pos)
            values.append(row[column_position-1])
        return values;

    def get_copy_struct(self, ): # ok
        struct = StructExcel()
        struct.import_params(self.export_params())
        return struct;

    def save_excel(self, excel_name: str, tab_name: str, folder: str = '.') -> str:
        save_excel = SaveExcel(excel_name, folder)
        save_excel.add_tab(tab_name, self)
        save_excel.save();
        return save_excel.get_filepath()
