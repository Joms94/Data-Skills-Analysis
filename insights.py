'''
Draws insights from the data.
'''
import pandas as pd
from database_interaction import get_records_from_database, upload_to_database


# Searches body text for list elements and sums occurrences by element.
def count_body_words(list:list, 
                     columns:list, 
                     sheetname:str, 
                     upload:bool=False, 
                     case_sensitivity:bool=True):
    data = get_records_from_database()
    word_dict = {}
    for element in list:
        word_dict.update({element: sum(data['Body'].str.contains(element, case=case_sensitivity))})
    wordcount_frame = pd.DataFrame.from_dict(data=word_dict, orient='index', dtype='int').sort_values(by=0, ascending=False)
    wordcount_frame.reset_index(inplace=True)
    wordcount_frame.columns = columns
    if upload == True:
        upload_to_database(dataframe=wordcount_frame, sheetname=sheetname, clear=False)
        print(f'{sheetname} updated successfully.')
    return wordcount_frame


# Which tech skills are employers looking for?
def count_technologies():
    count_body_words(list=[
                            'Python', 'R ', 'SQL', 'Tableau', 'Power BI', 
                            'SAS', 'AdWords', 'Looker', 'dbt', 'LookML', 
                            'MySQL', 'NoSQL', 'Java', 'Azure', 'Oracle', 
                            'Teradata', 'Qlik', 'Hadoop', 'Scala', 'SparkSQL',
                            'Kafka', 'SSIS', 'Jupyter', 'Excel', 'DB2',
                            'SharePoint', 'PowerPoint', 'SSRS', 'Google Analytics',
                            'Google Sheets', 'Cognos'], 
                     columns=['Technology', 'No. Jobs'], 
                     sheetname='Technologies', 
                     upload=True, 
                     case_sensitivity=True)


# Which soft skills are employers looking for?           
def count_soft_skills():
    count_body_words(list=[
                            'Attention to Detail', 'Teamwork', 'Strong Communication', 
                            'Creative', 'Problem-Solving', 'Analytical', 'Strategic Thinker'], 
                     columns=['Soft Skill', 'No. Jobs'], 
                     sheetname='Soft_Skills', 
                     upload=True, 
                     case_sensitivity=False)


# Updates database with answers to key analysis questions based on current data.
def update_all_insights():
    count_technologies()
    count_soft_skills()
    print('Insights updated.')


if __name__ == '__main__':
    update_all_insights()
