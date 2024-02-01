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

OH_files = [file for file in os.listdir(elec_folder_path) if os.path.isfile(os.path.join(elec_folder_path, file)) and file.startswith('OH')]

#create empty list to hold OH formatted dataframes
formatted_OH = [] 
OH_names = []

# Format Ohio election data
print("Formatting Ohio election data")
for i in OH_files: # Call item in the file list
    file = pd.read_excel(f'{elec_folder_path}/{i}', sheet_name='U.S. Congress', header=1) #minor pre-processing was required due to inconsistencies in OH SoS formatting
    
    # Apply the Ohio formatting function
    formated = format_OH(file)
    
    # Generate a name for each dataframe based on the filename without the file extension
    name = f'{i}' 
    name = name[:-5]+'_f' 
    
    # Assign the dataframe to the variable name
    globals()[name] = formated # from the documentation: 'the globals() function is a built-in function that returns a dictionary representing the current global symbol table' only half understand this, but it works (#programming)
    
    # Append both to the empty list creating a list of names and corresponding dataframes
    formatted_OH.append(formated)
    OH_names.append(name)

# Create zipped list of formatted State Election data, FEC list of candidates and parties, and the filenames found in raw_elec data
zipped_OH_FEC = zip(formatted_OH, FEC_files, OH_names)


# Further process and transform election data, grouping vote totals by party and incumbancy
print("Transforming Ohio Election Data")
# Allows analysis on these two metrics
for i, j, k in zipped_OH_FEC:
    
    # Joins FEC and State data for each year, produces list of counties as well
    # If an error is generated here, there is likely a mismatch between the counties in these files
    formatted_OH_FEC, counties = state_join_FEC(i,j)
    transformed_data = state_trans(formatted_OH_FEC, counties)
    
    # Writes the transformed data to a .csv file whose name references the original filename
    transformed_data.to_csv(fr"../data/formatted_house_totals/{k[:7]}.csv", index=False)
    
print("Data Successfully written to '/data/formatted_house_totals/'")