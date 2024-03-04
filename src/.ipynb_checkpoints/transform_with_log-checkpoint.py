### Due to the magnitude of the values in the IRS and Election data and the number of outliers resulting from this, taking the logarithm as a means to reduce the impact of these outliers is an important step before attempting to model the data with machine learning algorithms.

# Libraries for getting the data
import numpy as np
import pandas as pd
# from docx import Document
from modules import * #contains functions used in common with processing election and IRS data
import os

# Filepath to our formatted datasets (see 'merge_State_IRS_data.py' for how these were generated)
datasets_filepath = '../data/house_fec_irs_joined/' 

# datasets= [file for file in os.listdir(datasets_filepath) if os.path.isfile(os.path.join(datasets_filepath, file))]

### NOTE: Due to the nameing conventions used in merge_State_IRS_data.py, every even-indexed dataframe ([0),[2],[4],[6]..(etc. etc.) will be the election data merged with the IRS data from that year
### Every odd-indexed dataframe will contain the election data for that year merged with the IRS data from that year LESS the values from the previous year.

# Name an empty dataframe for the .csvs containing only IRS data from the year of the election
house_IRS_f = pd.DataFrame()

# get list of formatted filenames
formatted_IRS_house = [file for file in os.listdir(datasets_filepath) if os.path.isfile(os.path.join(datasets_filepath, file)) and file.endswith('irs.csv')]

print("Reading formatted IRS and Election data")
# Iterate through the list of csv files, merging the appropriate ones
for i in range(len(formatted_IRS_house)): # Iterated through the files in '../data/house_fec_irs_joined/' which only have the formatted data from that year
    
    csv_file = formatted_IRS_house[i]
    # Get filename for every even-numbered index
    data = pd.read_csv(os.path.join(datasets_filepath, csv_file))
    # Concatinate the dataframe to the blank df named above
    house_IRS_f = pd.concat([house_IRS_f, data], axis=0, ignore_index=True)
    
# Drop any null columns (The number of columns in the IRS data increases year-to-year, bureaucratically)
house_IRS_f = house_IRS_f.dropna(axis=1)

# Name an empty dataframe for .csvs containing IRS data LESS the previous year's data
house_IRS_d = pd.DataFrame()

# get list of formatted filenames, with the difference from the previous year
difference_IRS_house = [file for file in os.listdir(datasets_filepath) if os.path.isfile(os.path.join(datasets_filepath, file)) and file.endswith('irs_d.csv')]


print("Reading formatted Delta IRS and Election data")
# Iterate through the list of csv files, merging the appropriate ones
for i in range(len(difference_IRS_house)): # Iterated through the files in '../data/house_fec_irs_joined/' which have the formatted data LESS the data from the previous year
    
    csv_file = difference_IRS_house[i] 
    # Read in the csv
    data = pd.read_csv(os.path.join(datasets_filepath, csv_file))
    # Concatinate the dataframe to the blank df named above
    house_IRS_d = pd.concat([house_IRS_d, data], axis=0, ignore_index=True)
    
# Drop any null columns (The number of columns in the IRS data increases year-to-year, bureaucratically)
# house_IRS_d = house_IRS_d.dropna(axis=1)

print("Formatting data")
# These columns are not needed for the machine learning portion
house_IRS_f2 = house_IRS_f.drop(['STATE','County'],axis=1)
house_IRS_d2 = house_IRS_d.drop(['STATE','County'],axis=1)

print("Taking the logarithm")
# Take the log of our data
house_IRS_f_log = house_IRS_f2.apply(np.log)
house_IRS_d_log = house_IRS_d2.apply(np.log)

print("removing log-inf values")
# replace any inf. values with zero values 
house_IRS_f_log = house_IRS_f_log.replace([np.inf, -np.inf, np.nan], 0)
house_IRS_d_log = house_IRS_d_log.replace([np.inf, -np.inf, np.nan], 0)

# Write data
house_IRS_f_log.to_csv('../data/logarithm_of_joined_data/house_IRS_f_log.csv', index=False)
house_IRS_d_log.to_csv('../data/logarithm_of_joined_data/house_IRS_d_log.csv', index=False)

print("Data written to '../data/logarithm_of_joined_data/'")