from datetime import datetime, timedelta
import requests
import pandas as pd
from io import StringIO
from producers.finance.sources.nyse.api import load_df_to_duckdb


def generate_date_strings(start_date = '20190101', end_date = 'yesterday', from_date_format = '%Y%m%d', to_date_format = '%d-%b-%Y'):

    yesterday = (datetime.now() - timedelta(days=1)).strftime(to_date_format)
    start_date = yesterday if start_date == 'yesterday' else start_date
    end_date = yesterday if end_date == 'yesterday' else end_date

    # Parse the input date strings into datetime objects
    try:
        # Parse the input date strings into datetime objects
        start_date = datetime.strptime(start_date, from_date_format)
        end_date = datetime.strptime(end_date, from_date_format)
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
        # only add to list if it is a weekday (monday-friday)
        if current_date.weekday() < 5:
            # Format the current date as 'YYYYmmdd'
            date_str = current_date.strftime(to_date_format)
            date_strings.append(date_str)
            
        # Move to the next day
        current_date += timedelta(days=1)
    
    return date_strings


def regsho_by_date(datestring, to_date_format, urlgen_func, max_retries=3, backoff_factor=1):
    '''
        Grabs reg sho threshold list data from multiple sources (NYSE and NASDAQ currently)

        Can be used inside regsho_by_date_range function to grab data for multiple days and load into db

        Args:

        datestring: the date you want data for. Must be formatted 
    '''

    url = urlgen_func(datestring)
    print(f"Grabbing data from url: {url}")
    retries = 0
    
    # Send request to server using generated URL
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Got successfull response from server.")
                # print(response['Content-Type'])
                data = StringIO(response.text)
                df = pd.read_csv(data, sep='|')
                # Remove the last line  which is only datestring
                df = df.iloc[:-1]
                # Add the date as a new column
                try:
                    print("Adding date and source URL as columns")
                    # Convert date from supplied datestring to standard ISO format (using whatever date format was chosen for converting datestrings)
                    df['Date'] = pd.to_datetime(datestring, format=to_date_format).strftime('%Y-%m-%d')
                    df['Source URL'] = url
                except Exception as e: 
                    print(e)
                # Lazy solve for problem of duplicate column being created -- come back and find a better fix
                try: df = df.drop(columns=['Filler.1']) 
                except: pass

                return df  # Return the dataframe if successful

            elif response.status_code == 404:
                print(f"Error 404: Data not found for {datestring}.")
                return None  # Exit if data is not found
            else:
                print(f"Received status code {response.status_code}. Retrying...")
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
        retries += 1
        time.sleep(backoff_factor * retries)  # Exponential backoff
    
    print("Max retries reached. Failed to fetch data.")
    return None


def regsho_by_range(start_date, end_date, urlgen_func, table_name, db_path, from_date_format, to_date_format):
    '''
    Downloads NASDAQ or NYSE RegSHO data files for a range of dates

    Only difference is the URL and date formatting. Table Schema is the same

    Depends on: generate_date_strings(), download_and_unzip()

    Args:
    start_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)
    end_date: String

    Returns: df of values that failed to load into DuckDB

    '''

    # Allow 'yesterday' to be supplied as an input for start or end date
    # If start date is set to 'yesterday' a list of one day (yesterdays date) should be returned
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # Function requires string input so use strftime to convert
    start_date = yesterday if start_date == 'yesterday' else start_date
    end_date = yesterday if end_date == 'yesterday' else end_date

    # Gather properly formated list of datestrings (e.g. "YYYY_MM_dd"to feed into download url string 
    datestrings = generate_date_strings(start_date, end_date, from_date_format, to_date_format)
    print(f"Pulling data for the following dates: {list(datestrings)}")
    dfs=[]
    for datestring in datestrings:
        # Download file
        try: 
            print(f"Downloading data for date: {datestring}")
            df = regsho_by_date(datestring, to_date_format, urlgen_func)
            print(f"Pulled data for {datestring}: {df}")
            try:
                print("Loading to DuckDB...")
                load_df_to_duckdb(df, table_name, db_path)
            except Exception as e:
                print(e)
                print("Appending to dataframe to be returned...")
                dfs.append(df)

        except Exception as e:
            # print('\n\n',e)
            print(f"Could not grab data for date: {datestring} -- Probably tried to download a weekend or holiday date\n\n")

    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)

    return final_df