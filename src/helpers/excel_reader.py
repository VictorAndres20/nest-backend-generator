from typing import List
import pandas as pd
import base64
import io


def read_excel_to_list_dict(path_file: str) -> List:
    list_dict = []

    if path_file.endswith('.xlsx'):
        xls = pd.ExcelFile(path_file, engine='openpyxl')
    else:
        xls = pd.ExcelFile(path_file)
    for sheet_name in xls.sheet_names:
        if sheet_name != 'cg_type_col_params':
            df = pd.read_excel(xls, sheet_name=sheet_name, dtype=str)
            df = df.fillna("")
            module_dict = {sheet_name: []}
            for index, row in df.iterrows():
                module_dict[sheet_name].append({
                    'name': row['NAME'],
                    'type': row['TYPE'],
                    'column': row['COLUMN'],
                    'table_name': row['TABLE_NAME'],
                    'foreign_entity': row['FOREIGN_ENTITY'],
                    'fe_property': row['FE_PROPERTY'],
                    'fe_pk_type': row['FE_PK_TYPE'],
                    'fe_pk': row['FE_PK'],
                    'fe_module': row['FE_MODULE'],
                    'db_type': row['DB_TYPE'],
                    'default_value': row['DEFAULT_VALUE'],
                    'null': row['NULL'],
                })
            list_dict.append(module_dict)

    return list_dict


def read_excel_from_bytes(bytes_64: str, extension: str) -> pd.DataFrame:
    decrypted = base64.b64decode(bytes_64)
    toread = io.BytesIO()
    toread.write(decrypted)  # pass your `decrypted` string as the argument here
    toread.seek(0)  # reset the pointer
    if extension == 'xlsx':
        df = pd.read_excel(toread, engine='openpyxl')
    else:
        df = pd.read_excel(toread)
    df = df.fillna('')
    return df
