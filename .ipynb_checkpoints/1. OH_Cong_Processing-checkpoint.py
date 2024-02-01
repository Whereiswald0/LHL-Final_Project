import numpy as np
import pandas as pd
from src.modules import * #contains functions used in common with processing election and IRS data

import os #Used when reading/writing csv files programatically

# Get Ohio data taken from OH SoS page
ohio_2012_path = '../data/raw_elec_totals/ohio 2012precinct.xlsx'
excel_2012 = pd.ExcelFile(ohio_2012_path)
sheet_names_2012 = excel_2012.sheet_names

ohio_2014_path = 'data/raw_elec_totals/ohio 2014precinct.xlsx'
excel_2014 = pd.ExcelFile(ohio_2014_path)
sheet_names_2014 = excel_2014.sheet_names

ohio_2016_path = 'data/raw_elec_totals/ohio 2016precinct.xlsx'
excel_2016 = pd.ExcelFile(ohio_2016_path)
sheet_names_2016 = excel_2016.sheet_names

ohio_2018_path = 'data/raw_elec_totals/ohio 2018precinct.xlsx'
excel_2018 = pd.ExcelFile(ohio_2018_path)
sheet_names_2018 = excel_2018.sheet_names

ohio_2020_path = 'data/raw_elec_totals/ohio 2020precinct.xlsx'
excel_2020 = pd.ExcelFile(ohio_2020_path)
sheet_names_2020 = excel_2020.sheet_names

# See 'OH_Cong_data.ipynb' for data exploration, sheetnames obtained from there
# For future implementation, find programatic method for completing the following:

# Import Congressional Election Data for Ohio
print("reading OH Election data")

cong_OH_2012 = pd.read_excel(ohio_2012_path, sheet_name='U.S. Congress', header=1)
cong_OH_2014 = pd.read_excel(ohio_2014_path, sheet_name='Precinct-by-Precinct Results', header=1)
cong_OH_2016 = pd.read_excel(ohio_2016_path, sheet_name='U.S. Congress', header=1)
cong_OH_2018 = pd.read_excel(ohio_2018_path, sheet_name='U.S. Congress', header=1)
cong_OH_2020 = pd.read_excel(ohio_2020_path, sheet_name='U.S. Congress', header=1)

# Import Fed. Election Commision data regarding party affiliation
# FEC data is used to ensure consistency with party names and formatting
print("reading FEC Data")

fec_2012 = pd.read_csv(r'data\FEC\candidates_2012.csv', index_col=0)
fec_2014 = pd.read_csv(r'data\FEC\candidates_2014.csv', index_col=0)
fec_2016 = pd.read_csv(r'data\FEC\candidates_2016.csv', index_col=0)
fec_2018 = pd.read_csv(r'data\FEC\candidates_2018.csv', index_col=0)
fec_2020 = pd.read_csv(r'data\FEC\candidates_2020.csv', index_col=0)

#Note - We only want FEC data from the State being read - this is to avoid complications from having candidates with the same name running in house races in other States. 
### A more robust solution should be found in the future
fec_2012 = fec_2012.loc[fec_2012['STATE ABBREVIATION']=='OH']
fec_2014 = fec_2014.loc[fec_2014['STATE ABBREVIATION']=='OH']
fec_2016 = fec_2016.loc[fec_2016['STATE ABBREVIATION']=='OH']
fec_2018 = fec_2018.loc[fec_2018['STATE ABBREVIATION']=='OH']
fec_2020 = fec_2020.loc[fec_2020['STATE ABBREVIATION']=='OH']

# Format Ohio data to be joined to FEC
#This function will remove all unneeded datafields as well
print("processing OH data")

OH_2012_f = format_OH(cong_OH_2012)
OH_2014_f = format_OH(cong_OH_2014)
OH_2016_f = format_OH(cong_OH_2016)
OH_2018_f = format_OH(cong_OH_2018)
OH_2020_f = format_OH(cong_OH_2020)

# While it is VERY rare for a county to change names, this possibility should be accounted for in future versions
print("merging OH and FEC data")

OH_2012_f, OH_county_list12 = state_join_FEC(OH_2012_f, fec_2012)
OH_2014_f, OH_county_list14 = state_join_FEC(OH_2014_f, fec_2014)
OH_2016_f, OH_county_list16 = state_join_FEC(OH_2016_f, fec_2016)
OH_2018_f, OH_county_list18 = state_join_FEC(OH_2018_f, fec_2018)
OH_2020_f, OH_county_list20 = state_join_FEC(OH_2020_f, fec_2020)

# This funtion groups the data by party affiliation and prepares it to be joined to the IRS data
print("transforming OH data")

OH_2012_t = state_trans(OH_2012_f,OH_county_list12)
OH_2014_t = state_trans(OH_2014_f,OH_county_list12)
OH_2016_t = state_trans(OH_2016_f,OH_county_list12)
OH_2018_t = state_trans(OH_2018_f,OH_county_list12)
OH_2020_t = state_trans(OH_2020_f,OH_county_list12)

#Write those files to csvs
print("writing data to '..\data\formatted_house_totals'")

OH_2012_t.to_csv(r'data\formatted_house_totals\OH_House_12.csv', index=False)
OH_2014_t.to_csv(r'data\formatted_house_totals\OH_House_14.csv', index=False)
OH_2016_t.to_csv(r'data\formatted_house_totals\OH_House_16.csv', index=False)
OH_2018_t.to_csv(r'data\formatted_house_totals\OH_House_18.csv', index=False)
OH_2020_t.to_csv(r'data\formatted_house_totals\OH_House_20.csv', index=False)