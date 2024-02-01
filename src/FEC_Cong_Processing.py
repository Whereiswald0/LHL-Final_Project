import numpy as np
import pandas as pd
from modules import *
import os

# locate FEC files
fec_raw_folder_path = '../data/FEC/raw'
fec_raw_files = [file for file in os.listdir(fec_raw_folder_path) if os.path.isfile(os.path.join(fec_raw_folder_path, file))]

# Empty list to hold FEC files
FEC_files = []

# Process FEC files with FEC_simplifier (see modules.py)
print("Processing FEC files")
for i in fec_raw_files: 
    data = pd.read_excel(f"{fec_raw_folder_path}/{i}", sheet_name=f"20{i[6:8]} US House Results by State", header=0)
    simple_FEC_data = FEC_simplifier(data)
    # Generate a name for each dataframe based on the filename without the file extension
    name = f'{i[:9]}'
    simple_FEC_data.to_csv(fr"../data/FEC/{name}.csv", index=False)
print("Processed FEC files in '../data/FEC'")