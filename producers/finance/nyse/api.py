

import requests
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
import duckdb


def generate_date_strings(start_date, end_date):
    from_date_format = '%Y%m%d'
    to_date_format = '%d-%b-%Y'

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



def regsho_by_date(datestring, max_retries=3, backoff_factor=1):
    url = f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={datestring}&market=NYSE'
    retries = 0
    
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = StringIO(response.text)
                # print(response.text)
                df = pd.read_csv(data, sep='|')
                # Remove the last line  which is only datestring
                # timestamp = df.iloc[-1]
                df = df.iloc[:-1]
                # string_columns = ['Symbol', 'Security Name', 'Market Category', 'Reg SHO Threshold Flag']
                # for col in string_columns:
                #     if col in df.columns:
                #         df[col] = df[col].astype(str)
                # Add the date as a new column
                try:
                    print("Adding date as column")
                    df['Date'] = pd.to_datetime(datestring, format='%d-%b-%Y').strftime('%Y-%m-%d')
                except Exception as e: 
                    print(e)
                # df = df[['Symbol', 'Security Name', 'Market Category', 'Reg SHO Threshold Flag', 'Date']]

                # df['Symbol'] = df['Symbol'].astype(str)
                # df['Security Name'] = df['Security Name'].astype(str)
                # df['Market Category'] = df['Market Category'].astype(str)
                # df['Reg SHO Threshold Flag'] = df['Reg SHO Threshold Flag'].astype(str)
                df = df.drop(columns=['Filler.1'])

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


def load_df_to_duckdb(df, table_name, db_path):
    con = duckdb.connect(database=db_path, read_only=False)
    # Check if the table exists
    table_exists = con.execute(f"""
        SELECT count(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
    """).fetchone()[0] == 1

    # df['Symbol'] = df['Symbol'].astype(str)
    # df['Security Name'] = df['Security Name'].astype(str)
    df.reset_index(drop=True, inplace=True)

    if table_exists:
        # Insert data into the existing table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        # Create a new table and insert data
        con.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                Symbol VARCHAR,
                Security_Name VARCHAR,
                Market_Category VARCHAR,
                Reg_SHO_Threshold_Flag VARCHAR,
                Date DATE
                )
            """)
        con.execute(f"""
            INSERT INTO {table_name} SELECT * FROM df
        """)


def regsho_by_range(start_date, end_date, table_name, db_path):
    '''
    Downloads NYSE RegSHO data files for a range of dates

    Depends on: generate_date_strings(), download_and_unzip()

    Args:
    start_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)
    end_date: String

    Returns: df of values that failed to load into DuckDB

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
