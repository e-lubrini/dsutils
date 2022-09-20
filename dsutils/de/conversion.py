import csv, os
import pandas as pd
from dsutils.de.filesystem import  get_parent_dir

def xls_to_csv(xls_path, csv_path=''):
    read_file = pd.read_excel(xls_path)
    if not csv_path:
        csv_path = get_parent_dir(xls_path)+os.path.splitext(os.path.basename(xls_path))[0]
    read_file.to_csv (csv_path, index = None, header=True)
    return csv_path