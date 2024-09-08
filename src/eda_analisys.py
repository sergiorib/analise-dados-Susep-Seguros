# ============================================================
#  File:        Utilities.py
#  Author:      Sergio Ribeiro
#  Description: Various tools
# ============================================================
import json
import os
from pathlib import Path
import pandas as pd
from charset_normalizer import from_path 
from typing import Union
import config
from config import log_config
import csv

logger = log_config()

# ------------------------------------------------
# table level functions
# ------------------------------------------------

def file_size(table:str,file_path:str):
    try: 
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes == 0:
            return "0.00 B"
        BASE = 1024
        UNITS = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
        i = 0
        tamanho = float(file_size_bytes)
        while (tamanho >= BASE) and (i < len(UNITS) - 1):
            tamanho /= BASE 
            i += 1
        return f"{tamanho:.2f} {UNITS[i]}"
    except BaseException as e: 
        err_msg = f"file_size function error for ({table}): {str(e)}"
        logger.error(err_msg)
        return "err"

def lines(table:str,file_path:str):
    try: 
        encode_search = from_path(file_path).best() 
        encode = encode_search.encoding
        with open(file_path, "r", newline='', encoding=encode) as f:
            reader = csv.reader(f)
            row_count = sum(1 for _ in reader)
        return row_count
    except BaseException as e: 
        err_msg = f"lines function error for ({table}): {str(e)}"
        logger.error(err_msg)
        return "err"    

def columns(table:str,file_path:str,sep:str):
    try: 
        encode_search = from_path(file_path).best() 
        encode = encode_search.encoding   
        with open(file_path, "r", newline='', encoding=encode) as f:
            reader = csv.reader(f, delimiter=sep)
            col_count = len(next(reader))
        return col_count     
    except BaseException as e: 
        err_msg = f"columns function error for ({table}): {str(e)}"
        logger.error(err_msg)
        return "err"

def column_existance(table:str,file_path:str,sep:str):
    # missing_columns_lst = [] 
    # # open fields sheet to pick required ones 
    






    # df_expected_columns = (df_fields[df_fields['table'] == table_name]['field'].unique()) 
    # data_column_names = df_data.columns.to_list()
    # df_data_columns = pd.DataFrame({"column": data_column_names})
    # expected_set = set([c.strip().lower() for c in df_expected_columns])
    # data_set = set(df_data_columns['column'].str.strip().str.lower().tolist())
    # missing_colunms = expected_set.difference(data_set)
    # missing_columns_lst = list(missing_colunms)
    # if missing_colunms:
    #     str_missing_columns = ", ".join(sorted(list(missing_colunms)))
    # else:
    #     str_missing_columns = "nenhuma"





    return ""

def column_duplicity(table:str,file_path:str,sep:str):
    return ""

def column_uniquenes(table:str,file_path:str,sep:str):
    return ""

def pk_integrity(table:str,file_path:str,sep:str):
    return ""


