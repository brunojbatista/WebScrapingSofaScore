import pandas as pd
import re

class ReadingExcel():
    def __init__(self, excel_filepath: str) -> None:
        self.excel_filepath = excel_filepath
        self.list_sheets = []
        self.total_list_sheets = 0
        self.current_sheet = None;
        self.data = []
        self.column_position = 1
        self.row_position = 2

        self.read_list_sheets();

    def read_list_sheets(self, ):
        self.list_sheets = list(
            pd.read_excel(
                io=self.excel_filepath, 
                sheet_name=None
            ).keys()
        );
        self.total_list_sheets = len(self.list_sheets)

    def get_list_sheet(self, ) -> list:
        return self.list_sheets
    
    def get_total_list_sheet(self, ) -> int:
        return self.total_list_sheets
    
    def set_sheet(self, tab: str|int):
        target_sheet = None;
        if isinstance(tab, int):
            if tab > self.get_total_list_sheet() or tab <= 0:
                raise ValueError(f"A página da folha '{tab}' não existe")
            target_sheet = self.get_list_sheet()[tab-1]
        elif isinstance(tab, str):
            for sheet_name in self.get_list_sheet():
                if sheet_name != tab: continue;
                target_sheet = sheet_name
                break;
            if target_sheet is None:
                raise ValueError(f"O nome da folha '{tab}' não existe")
        else:
            raise ValueError(f"O nome da folha não é reconhecido")
        self.current_sheet = target_sheet
        self.read_sheet()
        return self;

    def read_sheet(self, ):
        self.data = []
        df = pd.read_excel(
            io=self.excel_filepath, 
            sheet_name=self.current_sheet, 
            keep_default_na=False
        );
        total_rows = len(df.index);
        if total_rows <= 0: raise ValueError(f"A folha '{self.current_sheet}' da planilha está vazia")
        columns = list(df.columns);
        self.data.append(columns)
        total_columns = len(columns)
        for row_index in range(0, total_rows):
            new_row = []
            for column_index in range(0, total_columns):
                cell = df[columns[column_index]][row_index]
                new_row.append(cell)
            self.data.append(new_row)
        self.set_start_column(1)
    
    def get_data(self, ):
        return self.data
    
    def set_start_column(self, pos: int):
        self.column_position = pos
        if pos <= 0: self.column_position = 0
        self.set_start_row(self.column_position+1)
        return self;
    
    def set_start_row(self, pos: int):
        self.row_position = pos
        return self;

    def get_column_position(self, ) -> int:
        return self.column_position
    
    def get_row_position(self, ) -> int:
        return self.row_position

    def get_columns(self, ) -> list:
        return self.data[self.get_column_position()-1]
    
    def get_rows(self, ) -> list:
        return self.data[(self.get_row_position()-1):]
    
