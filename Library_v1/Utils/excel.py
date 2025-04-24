import pandas as pd

import re;
from Library_v1.Utils.string import (
    clear_accents,
    default_lower,
)

from Library_v1.Directory.Directory import Directory

def get_content_excel(filepath_excel, start_row: int = 0):
    reading = {
        "columns": [], # Nome das colunas
        "data": [], # Lista de lista
    }

    if filepath_excel is None: raise ValueError("O caminho do excel é inválido")

    list_sheets = list(pd.read_excel(io=filepath_excel, sheet_name=None).keys());
    if len(list_sheets) <= 0: raise ValueError("Não existe nenhum folha definida no excel")
    first_sheet_name = list_sheets[0]
    # print(f"list_sheets: {list_sheets}")
    # print(f"first_sheet_name: {first_sheet_name}")

    df = pd.read_excel(
        io=filepath_excel, 
        sheet_name=first_sheet_name, 
        keep_default_na=False
    );

    total_rows = len(df.index);
    # print(f"total_rows: {total_rows}")
    if total_rows <= 0: raise ValueError("Planilha está vazia")
    columns = list(df.columns);
    total_columns = len(columns)
    # print(f"columns: {columns}")
    # print(f"total_columns: {total_columns}")

    # Criar o mapeamento das colunas
    named_columns_index = start_row - 1
    named_columns = []
    if named_columns_index < 0:
        named_columns = columns
    else:
        for col in columns:
            name_col = df[col][named_columns_index]
            named_columns.append(name_col)
    reading["columns"] = named_columns
    # print(f"named_columns: {named_columns}")

    start_row_index = start_row;
    start_column_index = 0;
    for row_index in range(start_row_index, total_rows):
        new_row = []
        for column_index in range(start_column_index, total_columns):
            data = df[columns[column_index]][row_index]
            new_row.append(data)
        reading["data"].append(new_row)

    return reading;

def create_excel(struct_excel: dict, name_excel: str, path = "."):
    columns = struct_excel["columns"]
    data = struct_excel["data"]

    print(f"columns: {columns} / total: {len(columns)}")

    prepared = {}
    for index_col, col in enumerate(columns):
        if col not in prepared: prepared[col] = []
        for row in data:
            input = row[index_col]
            prepared[col].append(input)

    df = pd.DataFrame(prepared)

    dir = Directory(path)
    writer = None;
    filepath = Directory.get_realpath(f"{dir.get_path()}/{name_excel}.xlsx")
    print(f">> filepath: {filepath}")
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Planilha1', startrow=1, header=False, index=False)

    worksheet = writer.sheets['Planilha1']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a list of column headers, to use in add_table().
    column_settings = []
    for header in df.columns: 
        column_settings.append({'header': header})

    # Add the table.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

    # Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def get_index_list(name_regex, columns: list):
    target_col_index = None;
    for col_index, col in enumerate(columns):
        if re.search(name_regex, clear_accents(col), flags=re.I):
            target_col_index = col_index;
            break;
    return target_col_index;