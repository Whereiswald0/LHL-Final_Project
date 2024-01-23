import numpy as np
import pandas as pd
from src.modules import * #contains functions used in common with processing election and IRS data

# Due to 'inconsistencies' with the way WI recorded their election data, this was done manually. 
### Find programatic method of selecting appropriate sheets
WI_12_sheets = ['Sheet3', 'Sheet4', 'Sheet5', 'Sheet6', 'Sheet7', 'Sheet8', 'Sheet9', 'Sheet10']
WI_14_sheets = ['Sheet6', 'Sheet7', 'Sheet8', 'Sheet9', 'Sheet10', 'Sheet11', 'Sheet12', 'Sheet13']
WI_16_sheets = ['Sheet2', 'Sheet3', 'Sheet4', 'Sheet5', 'Sheet6', 'Sheet7', 'Sheet8', 'Sheet9']
WI_18_sheets = ['Sheet2', 'Sheet3', 'Sheet4', 'Sheet5', 'Sheet6', 'Sheet7', 'Sheet8', 'Sheet9']
WI_20_sheets = ['Sheet2', 'Sheet3', 'Sheet4', 'Sheet5', 'Sheet6', 'Sheet7', 'Sheet8', 'Sheet9']

### Write programatic method of getting sheetnames and filepaths - see IRS Processing.py
print("reading WI election data")
excel_path_WI_12 = r'data/raw_elec_totals/wi 2012county.xlsx'
excel_path_WI_14 = r'data/raw_elec_totals/wi 2014county.xlsx'
excel_path_WI_16 = r'data/raw_elec_totals/wi 2016county.xlsx'
excel_path_WI_18 = r'data/raw_elec_totals/wi 2018county.xlsx'
excel_path_WI_20 = r'data/raw_elec_totals/wi 2020county.xlsx'

# will be used to programatically extract WI data in future
excel_path_list = [excel_path_WI_12, excel_path_WI_14, excel_path_WI_16, excel_path_WI_18, excel_path_WI_20]

# Get just the relevant sheets from the WI election data
print("processing WI election data")

WI_12_house = get_WI_data(WI_12_sheets,excel_path_WI_12)
WI_14_house = get_WI_data(WI_14_sheets,excel_path_WI_14)
WI_16_house = get_WI_data(WI_16_sheets,excel_path_WI_16)
WI_18_house = get_WI_data(WI_18_sheets,excel_path_WI_18)
WI_20_house = get_WI_data(WI_20_sheets,excel_path_WI_20)

# Format each dataframe
print("processing WI election data")

wi_house_12_f = format_WI(WI_12_house)
wi_house_14_f = format_WI(WI_14_house)
wi_house_16_f = format_WI(WI_16_house)
wi_house_18_f = format_WI(WI_18_house)
wi_house_20_f = format_WI(WI_20_house)

# Get the appropriate Federal Election data
print("reading FEC election data")

fec_2020 = pd.read_csv(r'data\FEC\candidates_2020.csv', index_col=0)
fec_2018 = pd.read_csv(r'data\FEC\candidates_2018.csv', index_col=0)
fec_2016 = pd.read_csv(r'data\FEC\candidates_2016.csv', index_col=0)
fec_2014 = pd.read_csv(r'data\FEC\candidates_2014.csv', index_col=0)
fec_2012 = pd.read_csv(r'data\FEC\candidates_2012.csv', index_col=0)

#Note - We only want FEC data from the State being read - this is to avoid complications from having candidates with the same name running in house races in other States. 
### A more robust solution should be found in the future
fec_2012 = fec_2012.loc[fec_2012['STATE ABBREVIATION']=='WI']
fec_2014 = fec_2014.loc[fec_2014['STATE ABBREVIATION']=='WI']
fec_2016 = fec_2016.loc[fec_2016['STATE ABBREVIATION']=='WI']
fec_2018 = fec_2018.loc[fec_2018['STATE ABBREVIATION']=='WI']
fec_2020 = fec_2020.loc[fec_2020['STATE ABBREVIATION']=='WI']

# Apply 'state_join_FEC' to each dataframe, producing a list of counties and the Election data with candidate party affiliation joined
print("joining WI election and FEC data")

wi_house_12_fec, wi_counties = state_join_FEC(wi_house_12_f, fec_2012)
wi_house_14_fec, wi_counties = state_join_FEC(wi_house_14_f, fec_2014)
wi_house_16_fec, wi_counties = state_join_FEC(wi_house_16_f, fec_2016)
wi_house_18_fec, wi_counties = state_join_FEC(wi_house_18_f, fec_2018)
wi_house_20_fec, wi_counties = state_join_FEC(wi_house_20_f, fec_2020)

# use 'state_trans' function to group election data by party affiliation, producing a dataframe with Counties as rows and party vote totals as columns
print("transforming dataframes")

WI_House_12_t = state_trans(wi_house_12_fec, wi_counties)
WI_House_14_t = state_trans(wi_house_14_fec, wi_counties)
WI_House_16_t = state_trans(wi_house_16_fec, wi_counties)
WI_House_18_t = state_trans(wi_house_18_fec, wi_counties)
WI_House_20_t = state_trans(wi_house_20_fec, wi_counties)

# Save those as CSVs
print("writing data to '..\data\formatted_house_totals'")

WI_House_12_t.to_csv(r'data\formatted_house_totals\WI_House_12.csv', index=False)
WI_House_14_t.to_csv(r'data\formatted_house_totals\WI_House_14.csv', index=False)
WI_House_16_t.to_csv(r'data\formatted_house_totals\WI_House_16.csv', index=False)
WI_House_18_t.to_csv(r'data\formatted_house_totals\WI_House_18.csv', index=False)
WI_House_20_t.to_csv(r'data\formatted_house_totals\WI_House_20.csv', index=False)