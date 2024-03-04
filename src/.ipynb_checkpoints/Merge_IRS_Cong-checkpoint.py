import numpy as np
import pandas as pd
from modules import *
import os

# Establish file paths for IRS data and the formatted vote totals for house races (See various State .py files)
irs_folder_path = '../data/irs_data/'
house_data_path = '../data/formatted_house_totals/'

# Using the OS library, create lists of all files
# There folders must be kept tidy, or incorrect data will be read
irs_files = [file for file in os.listdir(irs_folder_path) if os.path.isfile(os.path.join(irs_folder_path, file))]
house_data_files = [file for file in os.listdir(house_data_path) if os.path.isfile(os.path.join(house_data_path, file))]

# This block formats and merges the state election data with the IRS data from that election year
# In the current analysis, these files are not used, but this code block is retained as future analysis may make use of this to track corresponding changes in vote-totals and tax information
# With larger datasets this may become computationally expensive (since the same process is run below with differently-formatted IRS data)
# In this case, the block below should be commented out

print("Processing and merging IRS and Election data per year")
# 'county_check' will be used to evaluate any mismatches between the IRS and house data regarding county names
county_check = []
for i in house_data_files:
    state = i[0:2] #first two letters of the filename, corresponding to the state abbv.
    year = i[5:7] #two digit year 
    
    # Import house file
    house = pd.read_csv(f'{house_data_path}{i}')
    
    # Import IRS file corresponding to the year obtained from the filename of the house file
    # See 'IRS_Processing' .py file for how these are created
    irs = pd.read_csv(f'{irs_folder_path}irs_count_20{year}_f.csv')
    
    # Get IRS data only for the relevant state (this is done to ensure that states with identicle county names do not have their data mixed)
    irs_state = irs.loc[irs['STATE']==state]
    irs_county = irs_state['COUNTYNAME'].tolist()
    # irs_county = [i for i in remove_keyword(irs_county,'county')] # format to match the House data
    
    # Due to the length of some county names and the character limit of the 'COUNTYNAME' field in the original IRS data
    # some counties have 'County' displayed as 'Count', 'Coun' or 'Co'
    # Thus, the current solution will instead by to drop the final word
    irs_county = [' '.join(i.split()[:-1]) for i in irs_county]
    
    #These two counties are misnamed in the IRS data
    irs_misnamed = {'de witt':'dewitt','jo daviess':'jodaviess'}
    # This '.get's (haha) the correct county names
    cor_counties = [irs_misnamed.get(item, item) for item in irs_county]
    
    irs_copy = irs_state.copy() #avoid setting a value on a copy of a slice
    irs_copy['COUNTYNAME'] = cor_counties
    
    # Check if any county names do not match between the state data and the IRS data, if so, add to the 'county_check' list
    unmatched_counties = [county for county in irs_copy['COUNTYNAME'].tolist() if county not in house['County'].tolist()]
    if len(unmatched_counties) > 0:
        print(f"Counties mismatch in {i}")
        county_check.append('1')
    else:
        print(f"IRS data merged with {i}")
    
    irs_merge = house.merge(irs_copy, left_on='County', right_on='COUNTYNAME')
    
    # Drop columns for no-longer useful data,
    # In this case we don't need county names twice
    irs_export = irs_merge.drop('COUNTYNAME',axis=1)
    #Folder to store these new dataframes in
    new_folder_path = '../data/house_fec_irs_joined/'
    
    # Create the directory if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Save the DataFrames as CSV files
    csv_filename_f = f'{i[:-4]}_irs.csv'
    irs_export.to_csv(os.path.join(new_folder_path, csv_filename_f), index=False) #the 'final' formatted files, with election and IRS data combined
          
    if len(county_check) > 0:
        print("Errors in joining IRS and Election data, please resolve.")
    else:
        print("Data written to '../data/house_fec_irs_joined/'")

print("Processing and merging IRS LESS the data from the prevous year and the Election data")

# This block formats and merges the state election data with the IRS data from that election year LESS the IRS data from the previous year
# 'county_check' will be used to evaluate any mismatches between the IRS and house data regarding county names
county_check = []
for i in house_data_files:
    state = i[0:2] #first two letters of the filename, corresponding to the state abbv.
    year = i[5:7] #two digit year 
    
    # Import house file
    house = pd.read_csv(f'{house_data_path}{i}')
    
    # Import IRS file corresponding to the year obtained from the filename of the house file
    # See 'IRS_Processing' .py file for how these are created
    irs = pd.read_csv(f'{irs_folder_path}irs_count_20{year}_f_d.csv')
    
    # Get IRS data only for the relevant state (this is done to ensure that states with identicle county names do not have their data mixed)
    irs_state = irs.loc[irs['STATE']==state]
    irs_county = irs_state['COUNTYNAME'].tolist()
    # irs_county = [i for i in remove_keyword(irs_county,'county')] # format to match the House data
    
    # Due to the length of some county names and the character limit of the 'COUNTYNAME' field in the original IRS data
    # some counties have 'County' displayed as 'Count', 'Coun' or 'Co'
    # Thus, the current solution will instead by to drop the final word
    irs_county = [' '.join(i.split()[:-1]) for i in irs_county]
    
    #These two counties are misnamed in the IRS data
    irs_misnamed = {'de witt':'dewitt','jo daviess':'jodaviess'}
    # This '.get's (haha) the correct county names
    cor_counties = [irs_misnamed.get(item, item) for item in irs_county]
    
    irs_copy = irs_state.copy() #avoid setting a value on a copy of a slice
    irs_copy['COUNTYNAME'] = cor_counties
    
    # Check if any county names do not match between the state data and the IRS data, if so, add to the 'county_check' list
    unmatched_counties = [county for county in irs_copy['COUNTYNAME'].tolist() if county not in house['County'].tolist()]
    if len(unmatched_counties) > 0:
        print(f"Counties mismatch in {i}")
        county_check.append('1')
    else:
        print(f"IRS data merged with {i}")
    
    irs_merge = house.merge(irs_copy, left_on='County', right_on='COUNTYNAME')
    
    # Drop columns for no-longer useful data,
    # In this case we don't need county names twice
    irs_export = irs_merge.drop('COUNTYNAME',axis=1)
    #Folder to store these new dataframes in
    new_folder_path = '../data/house_fec_irs_joined/'
    
    # Create the directory if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Save the DataFrames as CSV files
    csv_filename_f = f'{i[:-4]}_irs_d.csv'
    irs_export.to_csv(os.path.join(new_folder_path, csv_filename_f), index=False) #the 'final' formatted files, with election and IRS data combined
          
    if len(county_check) > 0:
        print("Errors in joining IRS_d and Election data, please resolve.")
    else:
        print("Data written to '../data/house_fec_irs_joined/'")        
        
# print("Processing IRS data, calculating differnce from inter-election year, merging delta-IRS data and Election data")
# for i in house_data_files:
#     state = i[0:2] #first two letters of the filename, corresponding to the state abbv.
#     year = i[-6:-4] #two digit year 
    
#     # Import house file
#     house = pd.read_csv(f'{house_data_path}{i}')
    
#     # Import IRS file corresponding to the year obtained from the filename of the house file
#     irs = pd.read_csv(f'{irs_folder_path}irs_count_20{year}_f_d.csv')
    
#     # Get IRS data only for the relevant state (this is done to ensure that states with identicle county names do not have their data mixed)
#     irs_state = irs.loc[irs['STATE']==state]
#     irs_county = irs_state['COUNTYNAME'].tolist()
#     # irs_county = [i for i in remove_keyword(irs_county,'county')] # format to match the House data

#     # Due to the length of some county names and the character limit of the 'COUNTYNAME' field in the original IRS data
#     # some counties have 'County' displayed as 'Count', 'Coun' or 'Co'
#     # Thus, the current solution will instead by to drop the final word
#     irs_county = [' '.join(i.split()[:-1]) for i in irs_county]
        
#     #These two counties are misnamed in the IRS data
#     irs_misnamed = {'de witt':'dewitt','jo daviess':'jodaviess'}
#     cor_counties = [irs_misnamed.get(item, item) for item in irs_county]
    
#     irs_copy = irs_state.copy() #avoid setting a value on a copy of a slice
#     irs_copy['COUNTYNAME'] = cor_counties

#     irs_merge = house.merge(irs_copy, left_on='County', right_on='COUNTYNAME')
    
#     # Drop columns for no-longer useful data,
#     # In this case we don't need county names twice
#     irs_export = irs_merge.drop('COUNTYNAME', axis=1)
#     #Folder to store these new dataframes in
#     new_folder_path = '../data/house_fec_irs_joined/'
    
#     # Create the directory if it doesn't exist
#     os.makedirs(new_folder_path, exist_ok=True)
    
#     # Save the DataFrames as CSV files
#     csv_filename_f = f'{i[:-4]}_irs_d.csv'
#     irs_export.to_csv(os.path.join(new_folder_path, csv_filename_f), index=False) #the 'final' formatted files, with election and IRS data combined
    
#     # Compile the data into a single CSV
    
# print("data written to '../data/house_fec_irs_joined/'")