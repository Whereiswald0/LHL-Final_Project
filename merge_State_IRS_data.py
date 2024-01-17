import numpy as np
import pandas as pd
from src.modules import *
import os

irs_folder_path = 'data/irs_data/'
house_data_path = 'data/formatted_house_totals/'

irs_files = [file for file in os.listdir(irs_folder_path) if os.path.isfile(os.path.join(irs_folder_path, file))]
house_data_files = [file for file in os.listdir(house_data_path) if os.path.isfile(os.path.join(house_data_path, file))]

# This block formats and merges the state election data with the IRS data from that election year

for i in house_data_files:
    state = i[0:2] #first two letters of the filename, corresponding to the state abbv.
    year = i[-6:-4] #two digit year 
    
    # Import house file
    house = pd.read_csv(f'{house_data_path}{i}')
    
    # Import IRS file corresponding to the year obtained from the filename of the house file
    irs = pd.read_csv(f'{irs_folder_path}irs_count_20{year}_f.csv')
    
    # Get IRS data only for the relevant state (this is done to ensure that states with identicle county names do not hav their data mixed)
    irs_state = irs.loc[irs['STATE']==state]
    irs_county = irs_state['COUNTYNAME'].tolist()
    irs_county = [i.lower() for i in remove_keyword(irs_county,'County')] # format to match the House data
    
    #These two counties are misnamed in the IRS data
    irs_misnamed = {'de witt':'dewitt','jo daviess':'jodaviess'}
    cor_counties = [irs_misnamed.get(item, item) for item in irs_county]
    
    irs_copy = irs_state.copy() #avoid setting a value on a copy of a slice
    irs_copy['COUNTYNAME'] = cor_counties

    irs_merge = house.merge(irs_copy, left_on='County', right_on='COUNTYNAME')
    
    #drop columns for no-longer useful data,
    # In this case we don't need county names twice
    irs_export = irs_merge.drop('COUNTYNAME',axis=1)
    #Folder to store these new dataframes in
    new_folder_path = 'data/house_fec_irs_joined/'
    
    # Create the directory if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Save the DataFrames as CSV files
    csv_filename_f = f'{i[:-4]}_irs.csv'
    irs_export.to_csv(os.path.join(new_folder_path, csv_filename_f), index=False) #the 'final' formatted files, with election and IRS data combined
    
# This block formats and merges the state election data with the IRS data from that election year LESS the IRS data from the previous year
for i in house_data_files:
    state = i[0:2] #first two letters of the filename, corresponding to the state abbv.
    year = i[-6:-4] #two digit year 
    
    # Import house file
    house = pd.read_csv(f'{house_data_path}{i}')
    
    # Import IRS file corresponding to the year obtained from the filename of the house file
    irs = pd.read_csv(f'{irs_folder_path}irs_count_20{year}_f_d.csv')
    
    # Get IRS data only for the relevant state (this is done to ensure that states with identicle county names do not hav their data mixed)
    irs_state = irs.loc[irs['STATE']==state]
    irs_county = irs_state['COUNTYNAME'].tolist()
    irs_county = [i.lower() for i in remove_keyword(irs_county,'County')] # format to match the House data

        
    #These two counties are misnamed in the IRS data
    irs_misnamed = {'de witt':'dewitt','jo daviess':'jodaviess'}
    cor_counties = [irs_misnamed.get(item, item) for item in irs_county]
    
    irs_copy = irs_state.copy() #avoid setting a value on a copy of a slice
    irs_copy['COUNTYNAME'] = cor_counties

    irs_merge = house.merge(irs_copy, left_on='County', right_on='COUNTYNAME')
    
    #drop columns for no-longer useful data,
    # In this case we don't need county names twice
    irs_export = irs_merge.drop('COUNTYNAME', axis=1)
    #Folder to store these new dataframes in
    new_folder_path = 'data/house_fec_irs_joined/'
    
    # Create the directory if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Save the DataFrames as CSV files
    csv_filename_f = f'{i[:-4]}_irs_d.csv'
    irs_export.to_csv(os.path.join(new_folder_path, csv_filename_f), index=False) #the 'final' formatted files, with election and IRS data combined