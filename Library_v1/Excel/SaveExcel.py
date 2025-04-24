import Library_v1.Excel.StructExcel as Struct
from Library_v1.Directory.Directory import Directory

import re
import pandas as pd

class SaveExcel():
    def __init__(self, name: str, folder: str = '.') -> None:
        self.dir = Directory()
        self.name = re.sub(r"(?<=\.)[^\.]+$", "", name);
        self.filename = f"{self.name}.xlsx"
        self.folderpath = self.dir.find_dir(folder)
        self.filepath = Directory.get_realpath(f"{self.folderpath}/{self.filename}")
        self.tabs = []

    def add_tab(self, tab_name: str, struct: Struct):
        columns = struct.get_columns()
        rows = struct.get_rows()
        prepared = {}
        for index_col, col in enumerate(columns):
            if col not in prepared: prepared[col] = []
            for row in rows:
                input = row[index_col]
                prepared[col].append(input)
        self.tabs.append((tab_name, pd.DataFrame(prepared)))

    def save(self, ):
        writer = pd.ExcelWriter(self.filepath, engine='xlsxwriter')
        for tab_name, df in self.tabs:
            df.to_excel(writer, sheet_name=tab_name, startrow=1, header=False, index=False)
            worksheet = writer.sheets[tab_name]
            (max_row, max_col) = df.shape
            column_settings = []
            for header in df.columns: 
                column_settings.append({'header': header})
            worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
            worksheet.set_column(0, max_col - 1, 12)
        writer.save()

    def get_filepath(self, ) -> str:
        return self.filepath

    