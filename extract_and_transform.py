'''
Handles extraction and transformation operations.
'''
import pandas as pd
from statistics import median
from pandas.core import series
from database_interaction import get_records_from_database, update_worksheet
import re


# Finds dictionary values in text and replaces data with associated keys at cell range.
def dictionary_search(dict_input:dict, series_input:series, upload_range:str, na_text:str='NA', credentials_fname:str='credentials.json'):
    df = pd.DataFrame(columns=['Data'], index=(range(0, len(series_input))))
    for index, value in enumerate(series_input):
        for key in dict_input:
            for dict_value in dict_input[key]:
                if dict_value in value:
                    df['Data'][index] = key
    df.fillna(na_text, inplace=True)
    update_worksheet(
                    credentials_fname=credentials_fname, 
                    series_input=series_input, 
                    data=df['Data'], 
                    upload_range=upload_range)


# Searches 'Location' column of database, extracts the state and uploads it.
def find_state():
    dictionary_search(
                    dict_input={
                                'NSW': ['New South Wales', 'NSW', 'Sydney'],
                                'VIC': ['Victoria', 'VIC', 'Melbourne'],
                                'QLD': ['Queensland', 'QLD', 'Brisbane'],
                                'NT': ['Northern Territory', 'NT', 'Darwin'],
                                'WA': ['Western Australia', 'WA', 'Perth'],
                                'TAS': ['Tasmania', 'TAS', 'Hobart'],
                                'ACT': ['Australian Capital Territory', 'ACT', 'Canberra'],
                                'SA': ['South Australia', 'SA', 'Adelaide']
                                },
                    series_input=get_records_from_database()['Location'],
                    upload_range='C2:C{}',
                    na_text='AUS')
    
    print('States updated successfully.')


# Finds mentions of tertiary qualifications; adds 'YES' to 'Degree Needed?' DB column if match found.
def find_qualifications():
    dictionary_search(
                    dict_input={'YES': ['Tertiary', 'tertiary', 'Degree', 'degree']},
                    series_input=get_records_from_database()['Body'],
                    upload_range='G2:G{}',
                    na_text='NO')
    
    print('Qualifications updated successfully.')


# Searches 'Body' column of database, extracts and cleans the salary, then uploads it.
def add_salaries_to_database():
    body_series = get_records_from_database()['Body']
    salary_df = pd.DataFrame(columns=['Salary'], index=(range(0, len(body_series))))

    # Getting all currency numbers.
    for index, body in enumerate(body_series):
        salary_df['Salary'][index] = re.findall('(?:[\£\$\€]{1}[,\d]+.?\d*)', body)

    # Turning currency strings into floats.
    replace_dict = {
                    '': ['$', ',', '(', ')', '-', '+', ' ', '/'],
                    '000': ['k', 'K'],
                    '000000': ['m', 'M'],
                    '000000000': ['b', 'B']
                    }
    dict_length = sum([len(x) for x in replace_dict.values()]) # Used to count remaining total replacements.
    for index, salary_list in enumerate(salary_df['Salary']):
        new_ilist = [] # Stores cleaned values at index.
        for salary in salary_list:
            value_index = 1 # Checks remaining iterations against dict_length.
            for key, values in replace_dict.items():
                for value in values:
                    if value_index != dict_length and value in salary:
                        salary = salary.replace(value, key)
                        new_ilist.append(salary)
                        value_index += 1
        salary_df['Salary'][index] = new_ilist

    # Applying assumptions to currencies.
    for index, salary_list in enumerate(salary_df['Salary']):
        new_ilist = []
        for salary in salary_list:
            try:
                # Assuming any single-digit number cannot be a salary.
                if float(salary) <= 9:
                    break
                # Assuming any currency value larger than $400k cannot be a salary.
                if float(salary) >= 400000:
                    break
                # Assuming any three-digit number above $200 is a daily rate. 
                if float(salary) <= 999 and float(salary) >= 200:
                    new_ilist.append(((float(salary) * 5) * 4.5) * 12)
                    new_ilist.remove(salary)
                # Assuming any amount under $200 is an hourly rate.
                if float(salary) < 200 and float(salary) > 9:
                    new_ilist.append((((float(salary) * 8) * 5) * 4.5) * 12)
                    new_ilist.remove(salary)
                # Assuming any amount between $1000 to $40k isn't a salary.
                if float(salary) >= 1000 and float(salary) <= 40000:
                    new_ilist.remove(salary)
                else:
                    new_ilist.append(float(salary))
            except ValueError:
                    pass
        if not new_ilist:
            salary_df['Salary'][index] = new_ilist
        else:
            salary_df['Salary'][index] = median(new_ilist)

    # Fill all remaining empty cells with NA.
    for index, salary in enumerate(salary_df['Salary']):
        if not salary:
            salary_df['Salary'][index] = 'NA'

    # Upload results.
    update_worksheet(
                credentials_fname='credentials.json', 
                series_input=body_series, 
                data=salary_df['Salary'], 
                upload_range='F2:F{}')

    print('Salaries updated successfully.')


# Runs all extractions and transformations.
def perform_all_transformations():
    add_salaries_to_database()
    find_state()
    find_qualifications()


if __name__ == '__main__':
    perform_all_transformations()
