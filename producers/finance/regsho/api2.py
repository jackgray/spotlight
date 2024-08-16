from datetime import datetime, timedelta
import requests
import pandas as pd
import json
from io import StringIO
import duckdb
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Required, List, Union
from datetime import datetime
import time
from clickhouse_connect import get_client as ch
import re

    
    

def regsho_by_range(start_date, end_date, data_sources, ch_settings):
    '''
    Args:
    start_date/end_date: String %Y%m%d aka YYYYmmdd (e.g. 20240125 = jan 25 2024)
    '''

    datestrings = generate_date_strings(start_date, end_date)    # Gather properly formated list of datestrings (e.g. "YYYY_MM_dd"to feed into download url string 
    
    print(f"\nPulling data for dates ranging: {start_date}-{end_date}")
    for datestring in datestrings:
        # Download file
        print(f"\n\n****** Downloading data for date: {datestring}")

        regsho_by_date(datestring=datestring, data_sources=data_sources, ch_settings=ch_settings)


def regsho_by_date(datestring, data_sources, ch_settings):
    '''
    Grabs records by date for all data sources supplied

    Args:
    data_sources: [List]; One or all of ['nyse', 'nasdaq', 'finra']
    datestring: Str; YYYYmmdd format
    '''

    dfs=[]
    for data_source in data_sources:
        table_name = 'regsho_daily'          # Easily change the table naming convention
        print(f"\n\n**** Pulling data from {data_source} for {datestring}")
        try:
            if data_source == 'finra':
                df = finra_by_date(datestring=datestring, ch_settings=ch_settings)
            elif data_source == 'cboe':
                df = cboe_by_date(datestring=datestring, ch_settings=ch_settings)
            elif data_source == 'nasdaq':
                df = nasdaq_by_date(datestring=datestring, ch_settings=ch_settings)
            elif data_source == 'nyse':
                df = nyse_by_date(datestring=datestring, ch_settings=ch_settings)
            else:
                print("\nERROR: No valid data source supplied\n\n")
                return

            df['Date'] = pd.to_datetime(datestring, format='%Y%m%d') #.strptime('%Y-%m-%d').   
            print(f"\n\nCleaning df \n{df.head(3)}")
            cleaned = clean_df(df=df, data_source=data_source)
            print(f"\n\nInserting cleaned df to Clickhouse\n", df.head(3))
            try:
                df_to_clickhouse(df=cleaned, table_name=table_name, settings=ch_settings)
                print("\n\nSuccess!")
            except Exception as e:
                print(e)
        
        except:
            continue

   

def cboe_by_date(datestring, ch_settings, max_retries=5, backoff_factor=1):
    date_format = '%Y-%m-%d'
    datestring = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
    url = f'https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/{datestring}/csv'

    print(f"Pulling from CBOE for date {datestring} at url: {url}")

    retries = 0
    # Send request to server using generated URL
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = StringIO(response.text)
                df = pd.read_csv(data, sep='|')
                df = df.iloc[:-1]   # Remove the last line  which is only datestring

                print("\nAdding date and source URL as columns")
                df['Date'] = pd.to_datetime(datestring, format=date_format)     # Convert date from supplied datestring to standard ISO format (using whatever date format was chosen for converting datestrings)
                df['Source URL'] = url
                return df
             
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


def finra_by_date(ch_settings, datareq_type='data', group='otcmarket', dataset='thresholdlist', datestring='20240704', limit=1000) -> Optional[Union[List[dict], List]]:
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
    load_dotenv() # Load environment variables
    api_key = getenv('FINRA_API_KEY')
    api_secret = getenv('FINRA_API_SECRET')

    # Generate FINRA API session token
    token = get_finra_session(api_key, api_secret)
    if not token:
        print("\nToken for FINRA API could not be generated.")
        return

    url = f"https://api.finra.org/{datareq_type}/group/{group}/name/{dataset}"
    date_format = '%Y-%m-%d'
    datestring = f'{datestring[:3]}-{datestring[4:5]}-{datestring[6:7]}' # this is faster than datetime.strptime(datestring, '%Y%m%d').strftime(date_format)

    print(f"\nQuerying FINRA API at {url} for date {datestring}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    all_data = []
    offset = 0
    df = pd.DataFrame()
    while True:
        # This part allows date filtering
        params = {
            "limit": limit,
            "offset": offset,
            "compareFilters": [{ "fieldName": "tradeDate", "compareType": "equal", "fieldValue": datestring}]
        }
        print(f"With params: {params}")

        response = requests.post(url, headers=headers, json=params)     # Note: the request type must be POST for filtering the query

        if response.status_code == 200:
            response.raise_for_status()
            if response.headers.get('Content-Type') == 'text/plain':
                csv_data = StringIO(response.text)
                reader = csv.DictReader(csv_data)
                data = list(reader)
            else:
                data = response.json()
            if not data:
                print('No data returned from FINRA API')
                break

            all_data.extend(data)

            if len(data) < limit:   # requests next chuck until the data returned is less than the chuck requested
                break   
            offset += limit     # Limits throttle the request size to comply with usage rate agreement, offset moves through available data in chunks. Offset increments should be equal to limit
        else:
            print(f"Failed to fetch group {group} dataset {dataset} for date {datestring}: {response.status_code} {response.text}")
            return
    
    df = pd.DataFrame(all_data)
    df['Source URL'] = url

    return df

def nasdaq_by_date(datestring, ch_settings, max_retries=3, backoff_factor=1):
    ''' datestring must be in format YYYYmmdd '''

    date_format = '%Y%m%d'
    date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)

    url =f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{date}.txt'

    print(f"Grabbing data from url: {url}")
    retries = 0    
    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            data = StringIO(response.text)
            df = pd.read_csv(data, sep='|')
            df = df.iloc[:-1]  # Remove the last line  which is only datestring
            df['Source URL'] = url

            if len(df) < 3: # bail if df is too small to have real data
                return
            else:
                return df

        elif response.status_code == 404:
            print(f"Error 404: Data not found for {datestring}.")
            return
        else:
            print(f"Received status code {response.status_code}. Retrying...")

        retries += 1
        time.sleep(backoff_factor * retries)  # Exponential backoff
        
    print("Max retries reached. Failed to fetch data.")

    return


def nyse_by_date(datestring, ch_settings, markets=None, max_retries=3, backoff_factor=1):
    '''
        Grabs reg sho threshold list data from all NYSE markets (.self, American, and Arca)

        Args:
        datestring: the date you want data for. YYYYmmdd
        markets: List of NYSE markets to search; any combination of ['NYSE', 'NYSE%20Arca', 'NYSE%20American']
    '''
    print(f"\nPulling NYSE data for {datestring}")
    if not markets:
        markets = ['NYSE', 'NYSE%20Arca', 'NYSE%20American']
        print("Setting markets to pull from:", markets)
    
    date_format = '%d-%b-%Y'    # Format that the url query string expects
    date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
    
    all_data = pd.DataFrame()

    # NYSE has 3 Exchanges/TRFs that report FTDs: NYSE, NYSE American, and NYSE Arca
    # This collects records from all of them before returning df (modify markets argument to limit)
    for market in markets:
        print("Pulling from NYSE market: ", market)
        
        url = f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={date}&market={market}'
        print(f"\nGrabbing data from url: {url}")
        retries = 0
        # Send request to server using generated URL
        while retries < max_retries:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"\nGot successful response from server.")
                    data = StringIO(response.text)
                    df = pd.read_csv(data, sep= '|')
                    print("Preview: ", df.head(3))
                    if not df.empty:
                        df = df.iloc[:-1]   # Remove the last line which is only datestring
                        print("\nAdding date, source URL, and market as columns")
                        df['Date'] = pd.to_datetime(datestring, format='%Y%m%d') #.strptime('%Y-%m-%d').            # Add the date as a new column
                        df['Source URL'] = url
                        df['Market'] = market.replace('%20', ' ')

                        # Append the DataFrame to the all_data DataFrame
                        all_data = pd.concat([all_data, df], ignore_index=True)
                        break  # Exit while loop after successful fetch     
                    else:
                        print("No data found")
                        break
                elif response.status_code == 404:
                    print(f"Error 404: Data not found for {datestring}.")
                    break  # Exit if data is not found
                else:
                    print(f"Received status code {response.status_code}. Retrying...")
            except requests.RequestException as e:
                print(f"Error fetching data from {url}: {e}")
            retries += 1
            time.sleep(backoff_factor * retries)  # Exponential backoff
        
        if retries >= max_retries:
            print("Max retries reached. Failed to fetch data.")

    # Check if all_data is still empty
    if not all_data.empty:
       return all_data


def clean_df(df, data_source='NYSE'):
    '''
    Field definitions:  
    Nasdaq: https://www.nasdaqtrader.com/Trader.aspx?id=RegShoDefs
    NYSE: follows the same schema :) (also I can't find a data dict for it)
    FINRA: https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock
    '''
 
    acceptable_sources = ['nyse', 'nasdaq', 'finra']
    if data_source.lower() == 'nyse':
        df['Data Provider'] = 'NYSE'
        # Make fields only provided by FINRA satisfy SQL dimension requirements
        df['FINRA Rule 4320 Flag'] = ''
        df['Rule 3210'] = ' '
        df['Threshold List Flag'] = ' '
    elif data_source.lower() == 'cboe':
        df['Data Provider'] = 'Cboe'
        df['Threshold List Flag'] = ' '
        df['Reg SHO Threshold Flag'] = ' '
        df['Rule 3210'] = ' '
        df['FINRA Rule 4320 Flag'] = ' '
        df['Market'] = 'BZX'
        df['Market Category'] = ''
        df.rename(columns={'CompanyName':'Security Name'}, inplace=True)
        print("Changed cboe df ", df)
    elif data_source.lower() == 'nasdaq':
        df['Market'] = 'Nasdaq'
        df['Data Provider'] = 'Nasdaq'
        df['Threshold List Flag'] = ' '
        df['FINRA Rule 4320 Flag'] = ' '
    elif data_source.lower() == 'finra':    # Convert FINRA field names to NASDAQ/NYSE equivalents
        df['Data Provider'] = 'FINRA'
        df['Rule 3210'] = ' '
        column_map = {
            'tradeDate': 'Date',
            'issueSymbolIdentifier': 'Symbol',
            'issueName': 'Security Name',
            'marketClassCode': 'Market Category',
            'marketCategoryDescription': 'Market',
            'thresholdListFlag': 'Threshold List Flag',
            'regShoThresholdFlag': 'Reg SHO Threshold Flag',
            'rule4320Flag': 'FINRA Rule 4320 Flag'
        }

        print(f"\nRenaming column names of df: {df.columns} \n according to this map: {column_map}")
        df.rename(columns=column_map, inplace=True)
        print(f"\nRename successful - new column names: {df.columns}")
    else: 
        print(f"\nReceived unknown data source value: {data_source}. Please use one of {acceptable_sources}")
    

    drop_cols = [col for col in ['Filler', 'Filler.1'] if col in df.columns]    # NYSE/NASDAQ put in 'Filler' columns but don't use them. I haven't learned why yet, but we don't need to carry them over rn.
    df.drop(drop_cols, axis=1, inplace=True)    

    # Remove spaces to the right and left of all values (..is this needed?)
    # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Generate unique row ID programatically to avoid duplicate insertions
    print("\nGenerating ID string from data_source + Symbol + Date + Market Category")
    if len(df['Market Category'][0]) > 0:
        market_tag = df['Market Category'].str.replace(' ', '').str.lower()
    elif len(df['Market'][0])  > 0:
        market_tag = df['Market'].str.replace(' ', '').str.lower()
    else:
        print('No market identifier for ID formatting, need more unique points to make ID')
        return

    datestring = df['Date'].dt.strftime('%Y%m%d')

    df['ID'] = (data_source.lower() + df['Symbol'] + datestring + market_tag)

    df.reset_index(drop=True, inplace=True)    # drop the unecessary pandas index (which doesn't get inserted to duckdb)

    schema_mapping = {
        "ID": "str",
        "Date": "datetime64[ns]",
        "Symbol": "str",
        "Security Name": "str",
        "Market Category": "str",
        "Market": "str",
        "Reg SHO Threshold Flag": "str",
        "Threshold List Flag": "str",
        "FINRA Rule 4320 Flag": "str",
        "Rule 3210": "str",
        "Data Provider": "str",
        "Source URL": "str"
    }

    df = df.astype({col: dtype for col, dtype in schema_mapping.items() if col in df.columns})     # Assert data types for any df columns that exist in schema_mapping
    print("cleaned df:", df)

    return df


def create_table_from_df(df, table_name, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

    columns = []
    print(f"Creating clickhouse table for {table_name}, and generating schema from pandas dtypes")
    for col_name, dtype in zip(df.columns, df.dtypes):
        if "int" in str(dtype):
            ch_type = "Int64"
        elif "float" in str(dtype):
            ch_type = "Float64"
        elif "datetime64" in str(dtype):
            ch_type = "DateTime"
        elif "object" in str(dtype):
            ch_type = "String"
        else:
            ch_type = "String"  # Default to String for other types
        columns.append(f"`{col_name}` {ch_type}")
    print("Generated schema: ", columns)
    columns_str = ", ".join(columns)
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """
    ch_conn.command(create_table_query)
    print("\nTable created")

                     
def df_to_clickhouse(df, table_name, settings):
    print(f"\nConnecting to {settings['host']} table: {table_name} with settings\n{settings}")
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    df.columns = df.columns.str.replace(' ', '_')   # Remove spaces from column names

    create_table_from_df(df, table_name=table_name, settings=settings)
    print("\n\nInserting from df: ", df)
    ch_conn.insert_df(table_name, df)
    print("\nSuccess")


#########################
# Less interesting stuff
#########################

def generate_date_strings(start_date = '20190101', end_date='yesterday') -> Required[str]:
    '''
    Generates list of datestrings to supply to URL build parameters for API call

    Dates must be formatted as %Y%m%d aka YYYYmmdd; 'yesterday' will generate the datestring based on datetime.now
    '''
    date_format = '%Y%m%d'
    dates = { 'yesterday': (datetime.now() - timedelta(days=1)).strftime(date_format),
                'today': datetime.now().strftime(date_format) }
    start_date = dates.get(start_date, start_date)
    end_date = dates.get(end_date, end_date)

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


def get_finra_session(api_key: str, api_secret: str) -> Required[str]:
    """
    Retrieve a FINRA session token using the provided API key and secret.

    Parameters:
    api_key (str): The API key for FINRA you generated.
    api_secret (str): The API secret you set when you confirmed the API key creationA.

    Returns:
    Required[str]: The FINRA session token if the request is successful, otherwise None.
    """
    from base64 import b64encode

    # Encode the API key and secret
    finra_token = f"{api_key}:{api_secret}"
    encoded_token = b64encode(finra_token.encode()).decode()

    # URL for requesting the session token
    url = "https://ews.fip.finra.org/fip/rest/ews/oauth2/access_token?grant_type=client_credentials"
    headers = {
        "Authorization": f"Basic {encoded_token}"
    }

    try:
        # Make the request to get the session token
        response = requests.post(url, headers=headers)
    except Exception as e: print("Request for FINRA session token failed :( \n", e)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to get session token: {response.status_code} {response.text}")
        return None

