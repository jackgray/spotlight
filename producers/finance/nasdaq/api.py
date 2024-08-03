import requests
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta


def generate_date_strings(start_date, end_date):

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    start_date = yesterday if start_date == 'yesterday' else start_date
    end_date = yesterday if end_date == 'yesterday' else end_date

    # Parse the input date strings into datetime objects
    date_format = '%Y%m%d'
    try:
        # Parse the input date strings into datetime objects
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        print(f"Start date input: {start_date}")
        print(f"End date input: {end_date}")
        return []
    # Initialize an empty list to hold the date strings
    date_strings = []
    
    # Iterate over each day in the date range
    current_date = start_date
    while current_date <= end_date:
        # Format the current date as 'YYYYmmdd'
        date_str = current_date.strftime('%Y%m%d')
        date_strings.append(date_str)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return date_strings



def regsho_by_date(datestring):
    url = f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{datestring}.txt'
    response = requests.get(url)
    data = StringIO(response.text)
    df = pd.read_csv(data, sep='|')

    return df


def regsho_by_range(start_date, end_date):
    '''
    Downloads NASDAQ RegSHO data files for a range of dates

    Depends on: generate_date_strings(), download_and_unzip()

    Args:
    start_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)
    end_date: String

    '''

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # Function requires string input so use strftime to convert

    start_date = yesterday if start_date == 'yesterday' else start_date
    end_date = yesterday if end_date == 'yesterday' else end_date

    # Gather properly formated list of datestrings (e.g. "YYYY_MM_dd"to feed into download url string 
    datestrings = generate_date_strings(start_date, end_date)
    print(f"Pulling data for the following dates: {list(datestrings)}")
    dfs=[]
    for datestring in datestrings:
        # Download file
        try: 
            df = regsho_by_date(datestring)
            # print(df)
            dfs.append(df)

        except Exception as e:
            print('\n\n',e)
            print("Probably tried to download a weekend or holiday date")

    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)

    return final_df
