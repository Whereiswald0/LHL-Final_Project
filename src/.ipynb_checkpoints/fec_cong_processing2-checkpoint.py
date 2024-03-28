import numpy as np
import pandas as pd
from modules import *
import os 

# See the 'FEC_EDA' jupyter notebook for a walkthrough of the data being processed here

# Filepath to FEC raw data (data obtained from fec.gov)
fec_raw_folder_path = '../data/FEC/raw'

fec_raw_files = [file for file in os.listdir(fec_raw_folder_path) if os.path.isfile(os.path.join(fec_raw_folder_path, file))]

#Empty list to hold raw FEC data for processing, while generating filenames for formatted data
fec_data = []
for i in fec_raw_files: 
    data = pd.read_excel(f"{fec_raw_folder_path}/{i}", sheet_name=f"20{i[6:8]} US House Results by State", header=0)
    name = i.split('.')[0]
    fec_data.append((name,data))

for year, i in fec_data:
    # Rename columns to simple format
    new_col_dic = {'(I) Incumbent Indicator':'(I)','District':'D', 'DISTRICT':'D'}
    # Drop all rows that received no votes in the general election, or do not have a first name
    i = i.dropna(subset=['GENERAL VOTES ','CANDIDATE NAME (First)']) 
    i = i.reset_index(drop=True)
    
    # Current columns needed
    keep_cols = ['STATE ABBREVIATION','D','CANDIDATE NAME (First)','CANDIDATE NAME (Last)','CANDIDATE NAME(f)','CANDIDATE NAME','PARTY','(I)','GENERAL VOTES ']
    
    # Apply new column names
    i_copy = i.rename(columns=new_col_dic).copy()
    if '(I) Incumbent Indicator' in i.columns:
        i['(I)'] = i[['(I) Incumbent Indicator']]
    else:
        i = i.copy()
    # Convert incumbancy to binary value
    i_copy['(I)'] = i['(I)'].notna().astype(int)
    
    # Apply the two_party function (see modules.py)
    i_copy['PARTY'] = i.apply(two_party,axis=1)
    
    # Use trim_party (see modules.py) to remove middle names or titles stored in FEC First Names column
    i_copy['SIMPLE_FIRST'] = trim_party(i['CANDIDATE NAME (First)'],' ')
    
    # Create full name from first and last, transform to lower case to allow for easy comparison across datasets
    i_copy['CANDIDATE NAME(f)'] = i_copy['SIMPLE_FIRST']+' '+i_copy['CANDIDATE NAME (Last)']
    i_copy['CANDIDATE NAME(f)'] = i_copy['CANDIDATE NAME(f)'].astype(str).str.lower()
    
    # Remove all punctuation from candidate names
    cand_names = i_copy['CANDIDATE NAME(f)']
    cand_names = [''.join(char for char in i if char.isalpha() or char.isspace()) for i in cand_names]
    i_copy['CANDIDATE NAME(f)'] = cand_names
    
    # Keep only relevant columns
    i_copy = i_copy[keep_cols].copy()
    i_copy.to_csv(fr"../data/FEC/{year}.csv", index=False)