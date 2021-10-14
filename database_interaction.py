'''
For accessing and uploading records.
'''
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from pandas.core import series


# Upload a dataframe to a sheet in the database.
def upload_to_database(dataframe, sheetname='Main', clear=False):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('1Kl6DVkPDWsGionML58SyR-9i-Ls8oPOftSKdWObMqk4').worksheet(sheetname)
    if clear == True:
        sh.batch_clear(['A2:G'])
    set_with_dataframe(dataframe=dataframe, worksheet=sh)


# Upload a list to the main sheet of the database. Good for uploading data in pieces.
def upload_during_scrape(list, clear=False):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('1Kl6DVkPDWsGionML58SyR-9i-Ls8oPOftSKdWObMqk4')
    mainsheet = sh.sheet1
    if clear == True:
        mainsheet.batch_clear(['A2:G'])
    mainsheet.append_row(list)


# Displays all main sheet columns and rows in dataframe format.
def get_records_from_database():
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('1Kl6DVkPDWsGionML58SyR-9i-Ls8oPOftSKdWObMqk4')
    mainsheet = sh.sheet1
    res = mainsheet.get_all_records()
    return pd.DataFrame(data=res)


def drop_duplicates_from_database(drop_df:pd.DataFrame()=get_records_from_database(), sheetname:str='Main'):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('1Kl6DVkPDWsGionML58SyR-9i-Ls8oPOftSKdWObMqk4').worksheet(sheetname)
    drop_df.drop_duplicates(subset='Body', inplace=True, keep='first')
    sh.batch_clear(['A2:G'])
    set_with_dataframe(dataframe=drop_df, worksheet=sh)
    print(f'Duplicates dropped from {sheetname}.')


# Adds data to specified database columns.
def update_worksheet(credentials_fname:str, series_input:series, data, upload_range):
    gc = gspread.service_account(filename=credentials_fname)
    sh = gc.open_by_key('1Kl6DVkPDWsGionML58SyR-9i-Ls8oPOftSKdWObMqk4').worksheet('Main')
    table_length = len(series_input) + 1
    cell_list = sh.range(upload_range.format(table_length))

    for index, qual in enumerate([i for i in data]):
        cell_list[index].value = qual
    
    sh.update_cells(cell_list)


if __name__ == '__main__':
    get_records_from_database()
