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
import csv

# ------------------------------------------------
# table level functions
# ------------------------------------------------

def file_size(file_path:str):
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

def lines(file_path:str):
    encode_search = from_path(file_path).best() 
    encode = encode_search.encoding
    with open(file_path, "r", newline='', encoding=encode) as f:
        reader = csv.reader(f)
        row_count = sum(1 for _ in reader)
    return row_count

def columns(file_path:str,sep:str):
    encode_search = from_path(file_path).best() 
    encode = encode_search.encoding   
    with open(file_path, "r", newline='', encoding=encode) as f:
        reader = csv.reader(f, delimiter=sep)
        col_count = len(next(reader))
    return col_count     

