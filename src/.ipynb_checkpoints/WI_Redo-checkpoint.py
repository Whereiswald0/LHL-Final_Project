import numpy as np
import pandas as pd
from modules import *

import os #Used when reading/writing csv files programatically

fec_folder_path = '../data/FEC/'

fec_files = [file for file in os.listdir(fec_folder_path) if os.path.isfile(os.path.join(fec_folder_path, file))]

# Empty list to hold FEC files
FEC_files = []

# format FEC data
print('Formatting FEC data')
for i in fec_files: # Call item in the file list
    
    # Read each file from the FEC file list
    file = pd.read_csv(fr'{fec_folder_path}{i}', index_col=0)
    
    
    # Generate a name for each dataframe based on the filename without the file extension
    name = f'{i}' 
    name = name[:-4] 
    
    # Assign the dataframe to the variable name
    globals()[name] = file # from the documentation: 'the globals() function is a built-in function that returns a dictionary representing the current global symbol table' only half understand this, but it works (#programming)
    
    # Append both to the empty list
    FEC_files.append(file)

elec_folder_path = '../data/raw_elec_totals'

WI_files = [file for file in os.listdir(elec_folder_path) if os.path.isfile(os.path.join(elec_folder_path, file)) and file.startswith('WI')]

WI_sheets = ['Sheet2', 'Sheet3', 'Sheet4', 'Sheet5', 'Sheet6', 'Sheet7', 'Sheet8', 'Sheet9']

# Create empty lists to hold dataframes and their names
formatted_WI = []
WI_names = []

# Format Wisconsin election data
print("Formatting Wisconsin election data")
for i in WI_files: # Call item in the file list
    
    # Due to WI election data formatting, the get_WI_data function is needed to read the excel files and produce a single dataframe with all election data 
    file = get_WI_data(WI_sheets,f"{elec_folder_path}/{i}") 
    
    # Format data by applying format_WI
    formatted = format_WI(file)
    
    # Generate a name for each dataframe based on the filename without the file extension
    name = f'{i}' 
    name = name[:-5]+'_f' 
    
    # Assign the dataframe to the variable name
    globals()[name] = formatted # from the documentation: 'the globals() function is a built-in function that returns a dictionary representing the current global symbol table' only half understand this, but it works (#programming)
    
    # Append both to the empty list creating a list of names and corresponding dataframes
    formatted_WI.append(formatted)
    WI_names.append(name)

# Create zipped list of formatted State Election data, FEC list of candidates and parties, and the filenames found in raw_elec data
zipped_WI_FEC = zip(formatted_WI, FEC_files, WI_names)

# Further process and transform election data, grouping vote totals by party and incumbancy
print("Transforming Wisconsin Election Data")

for i, j, k in zipped_WI_FEC:
    
    # Joins FEC and State data for each year, produces list of counties as well
    # If an error is generated here, there is likely a mismatch between the counties in these files
    formatted_WI_FEC, counties = state_join_FEC(i,j)
    transformed_data = state_trans(formatted_WI_FEC, counties)
    
    # Writes the transformed data to a .csv file whose name references the original filename
    transformed_data.to_csv(fr"../data/formatted_house_totals/{k[:7]}.csv", index=False)
    
print("Data Successfully written to '/data/formatted_house_totals/'")