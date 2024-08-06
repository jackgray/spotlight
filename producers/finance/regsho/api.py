from datetime import datetime, timedelta
import requests
import pandas as pd
import json
from io import StringIO
import duckdb
from dotenv import load_dotenv
from os import getenv
from typing import Optional, List, Union
import time




def gen_nyse_regsho_url(datestring, market='NYSE'):
    '''
        Generates URL string from supplied date
        Expects datestring to be in the format dd-MonthAbrv-YYYY
        
        Usage:
        for datestring in generate_date_strings(start_date, end_date): 
            url = gen_nasdaq_regsho_url(datestring)

        Used in fetch functions to request the proper URL based on date format input parameters
    '''
    print("Converting datestring to expected format")
    datestring = datetime.strptime(datestring, '%Y%m%d').strftime('%d-%b-%Y')

    return f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={datestring}&market={market}'


def gen_nasdaq_regsho_url(datestring):
    '''
    Generates URL string from supplied date

    datestring expects format to be YYYYmmdd
    '''
    
    # datestring = datetime.strptime(datestring, '%Y%m%d').strftime('%Y%m%d')

    return f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{datestring}.txt'



def generate_date_strings(start_date = '20190101', end_date='yesterday'):
    '''
    Generates list datestrings to supply to URL build parameters for API call

    start_date: Input start date in format YYYYmmdd
    end_date: same format as above or 'yesterday' to automatically download up to the latest release
    date_format: the format that the data source URL uses. 
        Nasdaq: '%d-%b-%Y'
        NYSE: '%Y%m%d', 
        FINRA: '%Y-%m-%d'
    '''
    date_format = '%Y%m%d'
    yesterday = (datetime.now() - timedelta(days=1)).strftime(date_format)
    start_date = yesterday if start_date == 'yesterday' else start_date
    end_date = yesterday if end_date == 'yesterday' else end_date

    # Parse the input date strings into datetime objects
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
        # only add to list if it is a weekday (monday-friday)
        if current_date.weekday() < 5:
            # Format the current date as 'YYYYmmdd'
            date_str = current_date.strftime(date_format)
            date_strings.append(date_str)
            
        # Move to the next day
        current_date += timedelta(days=1)
    
    return date_strings



def get_finra_session(api_key: str, api_secret: str) -> Optional[str]:
    """
    Retrieve a FINRA session token using the provided API key and secret.

    Parameters:
    api_key (str): The API key for FINRA you generated.
    api_secret (str): The API secret you set when you confirmed the API ke creationA.

    Returns:
    Optional[str]: The FINRA session token if the request is successful, otherwise None.
    """
    from base64 import b64encode

    # Encode the API key and secret
    finra_token = f"{api_key}:{api_secret}"
    print(f"Using token: {finra_token}")
    encoded_token = b64encode(finra_token.encode()).decode()
    print(f"Using finra session token {encoded_token}")

    # URL for requesting the session token
    url = "https://ews.fip.finra.org/fip/rest/ews/oauth2/access_token?grant_type=client_credentials"
    headers = {
        "Authorization": f"Basic {encoded_token}"
    }

    # Make the request to get the session token
    response = requests.post(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to get session token: {response.status_code} {response.text}")
        return None




def fetch_finra_by_date(datareq_type='data', group='otcmarket', dataset='thresholdlist', datestring='20240704', limit=1000) -> Optional[Union[List[dict], List]]:
    """
    Query against FINRA Query API data from FINRA API for a specific date.

    Args:
    datareq_type: 'metadata' or 'data'
    group: the category that the dataset belongs to. Examples: otcmarket, fixedincomemarket
    dataset: the name of the dataset you want. Examples: treasuryweeklyaggregates, weeklysummary
    date_str: the date string in 'YYYY-MM-DD' format for which to fetch data
    limit: number of records to fetch per request, default is 1000

    Returns:
    Optional[Union[List[dict], List]]: data if the request is successful, otherwise None.
    """
    load_dotenv()
    # Load environment variables
    api_key = getenv('FINRA_API_KEY')
    api_secret = getenv('FINRA_API_SECRET')
    # Generate session token
    token = get_finra_session(api_key, api_secret)
    if not token:
        return None

    url = f"https://api.finra.org/{datareq_type}/group/{group}/name/{dataset}"
    # datestring = datetime.strptime(datestring, '%Y%m%d').strftime('%Y-%m-%d')

    print(f"Querying FINRA API at {url} for date {datestring}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    all_data = []
    offset = 0
    
    print(f"Requesting data for date: {datestring}")
    while True:
        params = {
            "limit": limit,
            "offset": offset,
            "compareFilters": [{ "fieldName": "tradeDate", "compareType": "equal", "fieldValue": datestring}]
        }

        print(f"With params: {params}")

        response = requests.post(url, headers=headers, json=params)

        if response.status_code == 200:
            response.raise_for_status()

            if response.headers.get('Content-Type') == 'text/plain':
                csv_data = StringIO(response.text)
                reader = csv.DictReader(csv_data)
                data = list(reader)
            else:
                data = response.json()

            if not data:
                break

            all_data.extend(data)   

            # print('Whats going on here: ', all_data)

            if len(data) < limit:
                break   # when there are fewer results than the limit we've reached the end

            offset += limit     # Move

        else:
            print(f"Failed to fetch group {group} dataset {dataset} for date {datestring}: {response.status_code} {response.text}")
            return None

    return pd.DataFrame(all_data)



def regsho_by_date(datestring, data_source, max_retries=3, backoff_factor=1):
    '''
        Grabs reg sho threshold list data from one of multiple possible sources (NYSE and NASDAQ currently)

        Can be used inside regsho_by_date_range function to grab data for multiple days and load into db

        Args:

        datestring: the date you want data for. Must be formatted 
        data_source: one of NYSE or Nasdaq
    '''

    # Set params
    if data_source.lower() == 'nyse':
        market = 'NYSE'
        date_format = '%d-%b-%Y'
        date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
        url = f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={date}&market={market}'

    elif data_source.lower() == 'nasdaq':
        date_format = '%Y%m%d'
        date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
        url =f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{date}.txt'
    
    elif data_source.lower() == 'finra':
        date_format = '%Y-%m-%d'
        date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
        df = fetch_finra_by_date(datestring=date)
        return df


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
                    df['Date'] = pd.to_datetime(datestring, format='%Y%m%d').strftime('%Y-%m-%d')
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


def clean_df(df, data_source='NYSE'):
    acceptable_sources = ['nyse', 'nasdaq', 'finra']
    if data_source.lower() == 'nyse':
        df['Source Entity'] = 'NYSE'
        df['Trade Type'] = 'OTC'
        df['FINRA Rule 4320 Flag'] = 'NA'
        df['Rule 3210'] = 'NA'
    elif data_source.lower() == 'nasdaq':
        df['Source Entity'] = 'Nasdaq'
        df['Trade Type'] = 'Non-OTC'
    elif data_source.lower() == 'finra':
        df['Source Entity'] = 'FINRA'
        df['Trade Type'] = 'OTC'
        df['Rule 3210'] = 'Y'
        column_map = {
            'tradeReportDate': 'Date',
            'securitiesInformationProcessorSymbolIdentifier': 'Symbol',
            'issueSymbolIdentifier': 'Symbol',
            'issueName': 'Security Name',
            'marketClassCode': 'Trade Type',
            'marketCategoryDescription': 'Market Category Description',
            'thresholdListFlag': 'Threshold List Flag',
            'regShoThresholdFlag': 'Reg SHO Threshold Flag',
            'rule4320Flag': 'FINRA Rule 4320 Flag'
        }



        print(f"Renaming column names of df: {df.columns} \n according to this map: {column_map}")
        try:
            df.rename(columns=column_map, inplace=True)
            print(f"Rename successful: {df.columns}")

        except Exception as e:
            print(e)
            print("Error cleaning df")
        
        print(f"Checking if datestring is the same as tradeDate: df: {df['Date']} ")
        df.drop('tradeDate', axis=1, inplace=True)

    else: 
        print(f"Received unknown data source value: {data_source}. Please use one of {acceptable_sources}")
    
    # Generate unique row ID
    print("Generating ID string")
    print(df.dtypes)

    df['ID'] = (data_source.lower() + df['Symbol'].str.lower() + 
            df['Date'].str.replace('-', '').str.replace('_', '') + df['Market Category'])

    # print(df['ID'])
    df.reset_index(drop=True, inplace=True)

    # Check for null values in the ID column
    null_ids = df['ID'].isnull()
    if null_ids.any():
        print("Null values found in ID column:")
        print(df[null_ids])


    return df
    

def load_df_to_duckdb(df, data_source, db_path):

    table_name = data_source.lower() + '_regsho_daily'

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    df = clean_df(df=df, data_source=data_source)

    print(f"Inserting cleaned dataframe: {df}")

    con = duckdb.connect(database=db_path, read_only=False)
    # Ensure the table exists with the correct schema
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            "ID" VARCHAR PRIMARY KEY,
            "Date" DATE,
            "Report Date" DATE,
            "Trade Date" DATE,
            "Symbol" VARCHAR,
            "Security Name" VARCHAR,
            "Market Category" VARCHAR,
            "marketClassCode" VARCHAR,
            "marketCategoryDescription" VARCHAR,
            "Reg SHO Threshold Flag" VARCHAR,
            "Threshold List Flag" VARCHAR,
            "FINRA Rule 4320 Flag" VARCHAR,
            "Rule 3210" VARCHAR,
            "shortParQuantity" VARCHAR, 
            "shortExemptParQuantity" VARCHAR, 
            "totalParQuantity" VARCHAR,
            "reportingFacilityCode" VARCHAR,
            "Filler" VARCHAR,
            "Source Entity" VARCHAR,
            "Source URL" VARCHAR,
            "Trade Type" VARCHAR
        )
    """

    try: con.execute(create_table_sql)
    except Exception as e: print(f"Could not make table {table_name} \n {e}")

    # Insert the data into the table
    insert_sql = f"""
        INSERT INTO {table_name} 
        SELECT * FROM df
        """
    try: con.execute(f"""
            INSERT INTO {table_name} BY NAME
            SELECT * FROM df
        """)
    except Exception as e: print(f'\n\nDB LOAD FAILED {e}\n\n')

    con.close()



def regsho_by_range(start_date, end_date, data_source, db_path):
    '''
    Downloads NASDAQ or NYSE RegSHO data files for a range of dates

    Only difference is the URL and date formatting. Table Schema is the same

    Depends on: generate_date_strings()

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
    datestrings = generate_date_strings(start_date, end_date)
    print(f"Pulling data for dates ranging: {start_date}-{end_date}")
    dfs=[]
    for datestring in datestrings:
        # Download file
        try: 
            print(f"Downloading data for date: {datestring}")
            df = regsho_by_date(datestring, data_source)
            print(f"Pulled data for {datestring}: {df}")
            try:
                print(f"Loading to DuckDB table for {data_source}...")
                load_df_to_duckdb(df=df, data_source=data_source, db_path=db_path)
            except Exception as e:
                print(e)
                print("Appending to dataframe to be returned...")
                dfs.append(df)

        except Exception as e:
            print('\n\n', e)
            print(f"Could not grab data for date: {datestring} -- Probably tried to download a weekend or holiday date\n\n")

    if len(dfs) > 0:
        # Concatenate all DataFrames into a single DataFrame
        final_df = pd.concat(dfs, ignore_index=True)

        return final_df
    else:
        return None



# def load_finra_regsho(datestring):
#     res = fetch_finra(type='data', group='otcmarket', dataset='regshodaily')
#     json_data = json.dumps(res, indent=2)
#     df = pd.read_json(json_data)
    
#     load_df_to_duckdb(df, 'finra', './gme.duckdb')

#     offset = 0
#     while True:
#         data = fetch_finra(date_str, offset=offset)
#         if not data:
#             break
#         all_data.extend(data)
#         offset += 1000  # Assuming the limit is 1000, adjust as necessary
#         if len(data) < 1000:
#             break  # Exit loop if the number of records is less than the limit
        

#     return df
