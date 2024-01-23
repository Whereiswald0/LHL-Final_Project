import numpy as np
import pandas as pd
from src.modules import * #contains functions used in common with processing election and IRS data

# ALL IL election data is formatted in a single sheet, making it very easy to get election data for any office
# In the future, an effort should be made to create similarly formatted sheets for every state.
il_2012_path = 'data/raw_elec_totals/IL_Gen_2012.xlsx'
excel_2012 = pd.ExcelFile(il_2012_path)
sheet_names_2012 = excel_2012.sheet_names

il_2014_path = 'data/raw_elec_totals/IL_Gen_2014.xlsx'
excel_2014 = pd.ExcelFile(il_2014_path)
sheet_names_2014 = excel_2014.sheet_names

il_2016_path = 'data/raw_elec_totals/IL_Gen_2016.xlsx'
excel_2016 = pd.ExcelFile(il_2016_path)
sheet_names_2016 = excel_2016.sheet_names

il_2018_path = 'data/raw_elec_totals/IL_Gen_2018.xlsx'
excel_2018 = pd.ExcelFile(il_2018_path)
sheet_names_2018 = excel_2018.sheet_names

il_2020_path = 'data/raw_elec_totals/IL_Gen_2020.xlsx'
excel_2020 = pd.ExcelFile(il_2020_path)
sheet_names_2020 = excel_2020.sheet_names

# Import Congressional Election Data for Illinois
### NOTE these lines generate warning about the headers and footers not being parsed. This does not seem to effect the data, but should be investigated. Pos. has something to do with the fileformat being changed from xsl to xslx?
print("reading IL Election data")
cong_IL_2012 = pd.read_excel(il_2012_path, sheet_name='TotalsByCounty',index_col=0)
cong_IL_2014 = pd.read_excel(il_2014_path, sheet_name='TotalsByCounty')
cong_IL_2016 = pd.read_excel(il_2016_path, sheet_name='TotalsByCounty')
cong_IL_2018 = pd.read_excel(il_2018_path, sheet_name='TotalsByCounty')
cong_IL_2020 = pd.read_excel(il_2020_path, sheet_name='TotalsByCounty')

# Get data for only congressional races
cong_IL_2012 = cong_IL_2012[cong_IL_2012['OfficeName'].str.contains('congress', case=False, na=False)]
cong_IL_2014 = cong_IL_2014[cong_IL_2014['OfficeName'].str.contains('congress', case=False, na=False)]
cong_IL_2016 = cong_IL_2016[cong_IL_2016['OfficeName'].str.contains('congress', case=False, na=False)]
cong_IL_2018 = cong_IL_2018[cong_IL_2018['OfficeName'].str.contains('congress', case=False, na=False)]
cong_IL_2020 = cong_IL_2020[cong_IL_2020['OfficeName'].str.contains('congress', case=False, na=False)]

# To be used when programatic approach to formatting dataframes is used
il_list = ['cong_IL_2012', 'cong_IL_2014','cong_IL_2016', 'cong_IL_2018', 'cong_IL_2020']
il_df_list = [cong_IL_2012, cong_IL_2014,cong_IL_2016, cong_IL_2018, cong_IL_2020]

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
fec_2012 = fec_2012.loc[fec_2012['STATE ABBREVIATION']=='IL']
fec_2014 = fec_2014.loc[fec_2014['STATE ABBREVIATION']=='IL']
fec_2016 = fec_2016.loc[fec_2016['STATE ABBREVIATION']=='IL']
fec_2018 = fec_2018.loc[fec_2018['STATE ABBREVIATION']=='IL']
fec_2020 = fec_2020.loc[fec_2020['STATE ABBREVIATION']=='IL']

# Format Illinois data to be joined to FEC
#This function will remove all unneeded datafields as well
print("processing OH data")

il_12_f = format_il(cong_IL_2012)
il_14_f = format_il(cong_IL_2014)
il_16_f = format_il(cong_IL_2016)
il_18_f = format_il(cong_IL_2018)
il_20_f = format_il(cong_IL_2020)

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
fec_2012 = fec_2012.loc[fec_2012['STATE ABBREVIATION']=='IL']
fec_2014 = fec_2014.loc[fec_2014['STATE ABBREVIATION']=='IL']
fec_2016 = fec_2016.loc[fec_2016['STATE ABBREVIATION']=='IL']
fec_2018 = fec_2018.loc[fec_2018['STATE ABBREVIATION']=='IL']
fec_2020 = fec_2020.loc[fec_2020['STATE ABBREVIATION']=='IL']

# Apply 'state_join_FEC' to each dataframe, producing a list of counties and the Election data with candidate party affiliation joined
print("joining IL election and FEC data")

il_house_12_fec, il_counties_12 = state_join_FEC(il_12_f, fec_2012)
il_house_14_fec, il_counties_14 = state_join_FEC(il_14_f, fec_2014)
il_house_16_fec, il_counties_16 = state_join_FEC(il_16_f, fec_2016)
il_house_18_fec, il_counties_18 = state_join_FEC(il_18_f, fec_2018)
il_house_20_fec, il_counties_20 = state_join_FEC(il_20_f, fec_2020)

# use 'state_trans' function to group election data by party affiliation, producing a dataframe with Counties as rows and party vote totals as columns
print("transforming dataframes")

il_house_12_t = state_trans(il_house_12_fec, il_counties_12)
il_house_14_t = state_trans(il_house_14_fec, il_counties_12)
il_house_16_t = state_trans(il_house_16_fec, il_counties_12)
il_house_18_t = state_trans(il_house_18_fec, il_counties_12)
il_house_20_t = state_trans(il_house_20_fec, il_counties_12)

# Save those as CSVs
print("writing data to '..\data\formatted_house_totals'")

il_house_12_t.to_csv(r'data\formatted_house_totals\IL_House_12.csv', index=False)
il_house_14_t.to_csv(r'data\formatted_house_totals\IL_House_14.csv', index=False)
il_house_16_t.to_csv(r'data\formatted_house_totals\IL_House_16.csv', index=False)
il_house_18_t.to_csv(r'data\formatted_house_totals\IL_House_18.csv', index=False)
il_house_20_t.to_csv(r'data\formatted_house_totals\IL_House_20.csv', index=False)