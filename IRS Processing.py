import numpy as np
import pandas as pd
from src.modules import * #contains functions used in common with processing election and IRS data

import os #Used when reading/writing csv files programatically

irs_raw_folder_path = 'data/irs_data/raw' 
irs_folder_path = 'data/irs_data/'

irs_raw_files = [file for file in os.listdir(irs_raw_folder_path ) if os.path.isfile(os.path.join(irs_raw_folder_path , file))]

# reverse the order, so the newest data is at the front of this list 
# No real need for this, but it helps with thinking about the values we're examining
# We want growth to be positive and loss to be negative to keep with the common understanding
irs_raw_files = irs_raw_files[::-1]

# Create empty list to hold tuples of filenames|dataframes
processed_irs_files = []

print("Formatting raw IRS data")
for i in irs_raw_files: # Call item in the file list
    file = pd.read_csv(f'{irs_raw_folder_path}/{i}', encoding='latin-1') #irs formatting requires this encoding
    file = file.drop(['STATEFIPS','AGI_STUB','COUNTYFIPS'],axis=1).reset_index(drop=True) # not used for the current analysis, but raw files are presevered for future use.
    
    # Lambda function to apply the filter line, removing all single name counties (should be agg. state data)
    filter_counties = lambda row: len(row['COUNTYNAME'].split()) >=2
    data_counties = file[file.apply(filter_counties, axis=1)]
    data_counties = [i.lower() for i in data_counties]
    
    # Generate a name for each dataframe based on the filename without the file extension
    name = f'{i}' 
    name = name[:-4]+'_f' 
    
    # Assign the dataframe to the variable name
    globals()[name] = data_counties # from the documentation: 'the globals() function is a built-in function that returns a dictionary representing the current global symbol table' only half understand this, but it works (#programming)
    
    # Append both to the empty list
    processed_irs_files.append((name, data_counties))
    
filtered_irs_files = [i[0] for i in processed_irs_files] # List of filenames
filtered_irs_dataframes = [i[1] for i in processed_irs_files] # List of dataframes
    # Didn't end up needing these, but they remain here as a comfort/future use

print("Processing IRS data, /n Writing IRS data to /irs_data")
for i in range(0, len(processed_irs_files), 2): # Call every-other item in the processed files list
    
    # Since these are from a list of tuples, we assign the dataframes to these variables, to be passed as arguments 
    arg1 = processed_irs_files[i][1] 
    arg2 = processed_irs_files[i + 1][1] if i + 1 < len(processed_irs_files) else None #if there is an odd number, it should throw an error, IMPLIMENT LATER

    # get the formatted irs file names for each year
    name = f'{processed_irs_files[i][0]}'
    
    # Run the function to subtract one year's data from the previous year's data
    prev_year_change(arg1, arg2) 
    df_diff = prev_year_change(arg1, arg2) # Placeholder variable
    new_df = f'{processed_irs_files[i][0]}_d' # Name of new variable
    
    # Create the directory if it doesn't exist
    os.makedirs(irs_folder_path, exist_ok=True)
    
    # Save the DataFrames as CSV files
    csv_filename_f = f'{name}.csv'
    csv_filename_d = f'{new_df}.csv'
    arg1.to_csv(os.path.join(irs_folder_path, csv_filename_f), index=False) #the 'original' formatted files
    df_diff.to_csv(os.path.join(irs_folder_path, csv_filename_d), index=False) #the file processed by the prev_year_change function