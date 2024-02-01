import pandas as pd
from docx import Document

def trim_party(data,delimiter='('):
    """this function will remove party designations for candidate names with the format used by the OH SoS, unless a different delimiter is called
    can also be used to split and return just first names from first name columns with middle names"""
    data_split = [cand.split(delimiter) for cand in data]
    cand_name = [cand[0] for cand in data_split]
    cand_name = [cand.strip() for cand in cand_name]
    return cand_name

def two_party(data):
    """this will reduce the parties to D for Democrat, R for Republican or 'Other' for any 3rd parties
    There is a joke here somewhere about 'tm is is how the political system actually works'"""
    if data['PARTY'] in ['R', 'D']:
        return data['PARTY']
    else:
        return "OTHER"
    
def remove_keyword(data, keyword):
    mod_list = []

    for i in data:
        if keyword in i:
            # Remove the keyword, strip, and add to the new list
            mod = i.replace(keyword, '').strip()
        else:
            # If the keyword is not present, keep the original entry
            mod = i

        mod_list.append(mod)

    return mod_list

def remove_middle_name(data):
    """this will return the start and end of a split item,
    built to remove middle names and titles from full name columns """
    no_middle = []
    for i in data:
        if len(i.split()) > 1:
            if i.split()[-1][-1] == '.': #will call the line below, skipping any titles appended to last names ending in '.'
                no_middle.append(i.split()[0] + ' ' + i.split()[-2])
            elif i.split()[-1].lower() == 'jr': #evauluating on .lower() ensures any changes in case between datasets will be ignored
                no_middle.append(i.split()[0] + ' ' + i.split()[-2])
            elif i.split()[-1].lower() == 'sr':
                no_middle.append(i.split()[0] + ' ' + i.split()[-2])
            else:
                no_middle.append(i.split()[0] + ' ' + i.split()[-1]) #default format is assumned to be 'Firstname Lastname'
        else:
            no_middle.append(i) #accounts for items without spaces, expected to be 'County' when applied to the assumed datasets.
    return no_middle

def FEC_simplifier(i):
    # Rename columns to simple format across all years
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
    
    # Keep only relevant columns
    i_copy = i_copy[keep_cols].copy()
    i = i_copy
    return i

def format_il(data):
    """
    This function is built to format election data 
    as recorded by the Illinois State Board of Elections
    Illinois produces records for the election as a whole rather than for individual offices
    """
    
    # Format names using 'trim party' function to remove middle names and titles, then concatinate so name matches FEC data
    data['CanFirstName'] = trim_party(data['CanFirstName'],' ') #removes middle names
    data['CanLastName'] = trim_party(data['CanLastName'], ' ') #removes titles appended to last names
    data['Candidate Name(f)'] = data['CanFirstName']+' '+data['CanLastName']
    #format names as lower-case
    data['Candidate Name(f)'] = data['Candidate Name(f)'].astype(str).str.lower()

    # Create list of candidates
    cand_list = data['Candidate Name(f)'].unique()

    #reduce candidate list to just names, if any name-final punctuation remains after removing titles
    cand_list = [''.join(char for char in i if char.isalpha() or char.isspace()) for i in cand_list] 

    # Since all races appear in a single sheet
    # Create tables for each candidate
    cand_tables = {}
    for i in cand_list:
        candidate_df = data[data['Candidate Name(f)'] == i][['County', 'Votes']]
        candidate_df = candidate_df.groupby('County').sum().reset_index()
        cand_tables[i] = candidate_df

    # Merge tables
    merged_df = cand_tables[cand_list[0]]
    for i in cand_list[1:]:
        merged_df = pd.merge(merged_df, cand_tables[i], on='County', how='outer', suffixes=('_' + i, ''))

    # Rename columns
    merged_df.columns = ['County'] + list(cand_list)

    # If candidate received zero votes, fill NaN
    merged_df = merged_df.fillna(0)
    return merged_df

def format_OH(data):
    """
    This function is build to prepare election data from the Ohio Sec. of State 
    """
    
    col_dic = {'County Name':'County'} #column names to reformat
    bad_counties = ['Total','Percentage'] #rows with totals rather than county data
    
    #remove general information about the election, we only want the details about each canddidate, OH marks candidates by party or * if write-in
    candidates = [i for i in data.columns if i.endswith(')') or i.endswith('*')] #gets list of candidates
    data = data.rename(columns=col_dic) 
    
    #Add the renamed 'County' column (always 1st column) to our list of candidates
    candidates.insert(0, data.columns[0])
    
    #use defined "bad terms" to remove unneeded information from the table
    data = data[~data['County'].isin(bad_counties)].copy()
    
    #future cases may want to split the flow here, to evauluate other races than House races
    data_copy = data[candidates].copy()
    
     #apply trim_party to get just candidate names w/o party designation
    data_copy.columns = trim_party(data_copy.columns)
    
    #ensure all column names will be compatable with the FEC data for future mergers
    ###
    ### NOTE - this step will be complicated for states that have candidates with the same first and last name running - edge cases, but must be accounted for in the future
    ###
    data_copy.columns = remove_middle_name(list(data_copy.columns))
    #OH reports by precinct, we only need data by 'County'
    data_copy = data_copy.groupby('County').sum().reset_index()
    return data_copy

def state_join_FEC(data, fec_data):
    """ 
    This function prepares and joins FEC data to the state election data
    """
    #for state data, first column is always County names
    county_col = data.columns[0]
    
    #county names will be reinserted later for the merger with IRS data
    counties = data[county_col].tolist()
    counties = [i.lower() for i in counties]
    data_t = data.drop(county_col, axis=1).copy()
    
    # Transpose the dataframe so that our columns are the county vote totals and candidates are rows
    # This is done to aid the transformation and grouping of candidates by party
    data_t=data_t.transpose()
    cand_list = list(data_t.index)
    
    # Render candidate names in lowercase to match FEC data
    cand_list = [i.lower() for i in cand_list]
    data_t.index = cand_list
    
    # Merge FEC data, associating each candidate with their party and incumbancy
    data_t = pd.merge(data_t, fec_data, left_index=True, right_on='CANDIDATE NAME(f)').reset_index(drop=True)
    
    # return dataframe of candidates and list of counties
    return data_t, counties

def state_trans(data, counties):
    
    # Group candidates by party and incumbancy
    grouped_data = data.groupby(['PARTY','(I)']).sum()
    
    # Keep only data from counties (these columns will be numeric, since they were named for the indices assigned by the OH_join_FEC function)
    drop_cols = [i for i in grouped_data.columns.tolist() if str(i).isnumeric()]
    fit_data = grouped_data[drop_cols]
    
    # Flatted the resulting multi-indexed dataframe
    result_data = fit_data.apply(lambda x: x.droplevel(1).T.reset_index(drop=True)).reset_index(drop=True)
    
    # Create a column based on the multi-indicies
    result_data['index'] = grouped_data.index.get_level_values('PARTY')+grouped_data.index.get_level_values('(I)').astype(str)
    
    # Transpose again, resetting the format to columns of candidates (reduced to party) and rows corresponding to counties
    reset_data = result_data.T
    reset_data.columns = reset_data.iloc[-1]
    reset_data = reset_data[:-1]
    cols = list(reset_data.columns)
    cols.insert(0,'County')
    reset_data['County'] = counties
    reset_data = reset_data[cols]
    return reset_data

def get_WI_data(sheet_names,filepath):
    
    """
    
    """

    col_dic = {'Unnamed: 0':'County'} #column names to reformat
    # bad_counties = ['total','percentage'] #rows with totals rather than county data
    data = pd.DataFrame()

    for i in sheet_names:
        d = pd.read_excel(filepath, sheet_name=i, header=5)
        data = pd.concat([data, d], ignore_index=True)
    # # Due to source formatting, 'Counties' column will appear unnamed when first imported, rename to counties:
    data = data.rename(columns=col_dic) 
    data = data.groupby('County').sum().reset_index()
    # lower_county  = [i.lower() for i in data['County'].tolist()]
    data['County'] = [i.lower() for i in data['County'].tolist()]
    data = data[~data['County'].str.contains('total')].copy()
    
    return data

def format_WI(data):
    drop_col = ['scattering','unnamed: 1', 'unnamed: 2'] #columns from original data to remove
    data_copy = data.copy()
    cols = data.columns.tolist()
    cols = [i.lower() for i in cols]
    
    # Drop party/write-in lables and remove middle names
    cols = trim_party(cols)
    cols = remove_middle_name(cols)
    
    # Keep only relevant columns
    data_copy.columns = cols
    data_copy = data_copy.drop(columns=drop_col)
    
    return data_copy

def prev_year_change(data1, data2):
    """
    This function will substitute the difference between a year and the previous year's IRS records, 
    Giving us the change-over-year and letting us use that as an indication of economic growth/loss
    
    NOTE: data1 should be the more recent year, data2 should be the older year.
    """
    
    # Create a set containing columns common to both dataframes 
    # Note for future use, the '&' here only keeps items that intersect both lists
    col_common = set(data1.columns) & set(data2.columns)
    
    #merge the dataframes, keeping data1 if the datatype is 'Object' or if the column is not in the set (all columns held in column should appear in the set..)
    merged = pd.concat([
        data1[c] if c not in col_common or data1[c].dtype == 'O' else data1[c] - data2[c]
        for c in data1.columns
    ], axis=1)
    
    return merged


def table_from_docx(docx_path):
    """
    This function reads in docx tables as dataframes.
    Will only take the first table. 
    This has been written with the IRS data in mind, 
    A more neutral version or one altered to account for other datasets would be ideal
    """
    
    # Define variables
    doc = Document(docx_path)
    tables = doc.tables #this method pulls all tables from the document, unsure what happens if it's called on a doc with multiple tables.

    data = {'Variable Name': [], 'Description': [], 'Value Line Ref': []}  # Adjust column names according to the IRS format
    
    #Build a number of lists containing the data from the table, attach each to a key in the dictionary above
    for table in tables:
        for row in table.rows:
            columns = row.cells
            data['Variable Name'].append(columns[0].text)
            data['Description'].append(columns[1].text)
            data['Value Line Ref'].append(columns[2].text)

    # Turn the dictionary into a dataframe and return it
    data_table = pd.DataFrame(data)
    return data_table

