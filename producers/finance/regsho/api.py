from datetime import datetime, timedelta
import requests
import pandas as pd
import json
from io import StringIO
import duckdb
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Required, List, Union
import time


def cboe_by_date(datestring, db_path='./stonk.duckdb', max_retries=5, backoff_factor=1):
    date_format = '%Y-%m-%d'

    try:
        datestring = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
    except Exception as e:
        print(e)
    url = f'https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/{datestring}/csv'

    print(f"Pulling from CBOE for date {datestring} at url: {url}")
    retries = 0
    # Send request to server using generated URL
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"\nGot successfull response from server.")
                # print(response['Content-Type'])
                data = StringIO(response.text)
                df = pd.read_csv(data, sep='|')
                # Remove the last line  which is only datestring
                df = df.iloc[:-1]
                # Add the date as a new column
                try:
                    print("\nAdding date and source URL as columns")
                    # Convert date from supplied datestring to standard ISO format (using whatever date format was chosen for converting datestrings)
                    df['Date'] = datestring
                    df['Source URL'] = url
                except Exception as e: 
                    print("\n\n\n********************\n", e, "\n********************\n\n")                # Lazy solve for problem of duplicate column being created -- come back and find a better fix
                
                # Load it into database
                df = load_df_to_duckdb(df=df, db_path=db_path, data_source='cboe')

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
    return df



def finra_by_date(datareq_type='data', group='otcmarket', dataset='thresholdlist', datestring='20240704', db_path='./stonk.duckdb', limit=1000) -> Optional[Union[List[dict], List]]:
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
        print("\nToken for FINRA API could not be generated.")
        return pd.DataFrame()  # Changed from None to an empty DataFrame

    url = f"https://api.finra.org/{datareq_type}/group/{group}/name/{dataset}"
    date_format = '%Y-%m-%d'
    datestring = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)

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

        response = requests.post(url, headers=headers, json=params)     # Note that the request type must be POST for filtering the query

        if response.status_code == 200:
            response.raise_for_status()

            # Extract response as CSV
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
            if len(data) < limit:
                # when there are fewer results than the limit we've reached the end and can break the while loop
                break   
           
           # Limits throttle the request size to comply with usage rate agreement, offset moves through available data in chunks. Offset increments should be equal to limit
            offset += limit     
        else:
            print(f"Failed to fetch group {group} dataset {dataset} for date {datestring}: {response.status_code} {response.text}")
            return pd.DataFrame()

    df = pd.DataFrame(all_data)
    print("Returning FINRA df (preview): ", df.head(3))
    df['Source URL'] = url
    df = load_df_to_duckdb(df=df, db_path=db_path, data_source='FINRA')
    return df


def nyse_by_date(datestring, markets=None, db_path='./stonk.duckdb', max_retries=3, backoff_factor=1):
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
                    df = pd.read_csv(data, sep='|')
                    print("Preview: ", df.head)
                    # Remove the last line which is only datestring
                    if not df.empty:
                        df = df.iloc[:-1]

                    # Add the date as a new column
                    if not df.empty:
                        try:
                            print("\nAdding date, source URL, and market as columns")
                            df['Date'] = pd.to_datetime(datestring, format='%Y%m%d').strftime('%Y-%m-%d')
                            df['Source URL'] = url
                            df['Market'] = market.replace('%20', ' ')
                        except Exception as e: 
                            print("\n\n\n********************\n", e, "\n********************\n\n")

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
        # Load results to database
        print(f"Loading NYSE data for date {datestring} into database: {df}")
        df = load_df_to_duckdb(df=all_data, db_path=db_path, data_source='NYSE')
    
    return df


def nasdaq_by_date(datestring, db_path, max_retries=3, backoff_factor=1):
    ''' datestring must be in format YYYYmmdd '''

    date_format = '%Y%m%d'
    date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
    url =f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{date}.txt'

    print(f"Grabbing data from url: {url}")
    retries = 0
    
    # Send request to server using generated URL
    while retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"\nGot successfull response from server.")
                # print(response['Content-Type'])
                data = StringIO(response.text)
                df = pd.read_csv(data, sep='|')
                # Remove the last line  which is only datestring
                df = df.iloc[:-1]
                # Add the date as a new column
                try:
                    print("\nAdding date and source URL as columns")
                    # Convert date from supplied datestring to standard ISO format (using whatever date format was chosen for converting datestrings)
                    df['Date'] = pd.to_datetime(datestring, format='%Y%m%d').strftime('%Y-%m-%d')
                    df['Source URL'] = url
                except Exception as e: 
                    print("\n\n\n********************\n", e, "\n********************\n\n")                # Lazy solve for problem of duplicate column being created -- come back and find a better fix
                
                # Load it into database
                df = load_df_to_duckdb(df=df, db_path=db_path, data_source='nasdaq')

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
    return df



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
        df['FINRA Rule 4320 Flag'] = ' '
        df['Market'] = 'BZX'
        df['Market Category'] = ''
        df.rename(columns={'CompanyName':'Security Name'}, inplace=True)
    elif data_source.lower() == 'nasdaq':
        df['Market'] = 'Nasdaq'
        df['Data Provider'] = 'Nasdaq'
        df['Threshold List Flag'] = ' '
        df['FINRA Rule 4320 Flag'] = ' '
    # Convert FINRA field names to NASDAQ/NYSE equivalents
    elif data_source.lower() == 'finra':
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
        try:
            df.rename(columns=column_map, inplace=True)
            print(f"\nRename successful - new column names: {df.columns}")

        except Exception as e:
            print("\n\n\n********************\n", e, "\n********************\n\n")
            print("\nError cleaning df")
    else: 
        print(f"\nReceived unknown data source value: {data_source}. Please use one of {acceptable_sources}")
    
    # NYSE/NASDAQ put in 'Filler' columns but don't use them. I haven't learned why yet, but we don't need to carry them over rn.
    drop_cols = [col for col in ['Filler', 'Filler.1'] if col in df.columns]
    df.drop(drop_cols, axis=1, inplace=True)

    # Generate unique row ID programatically to avoid duplicate insertions
    print("\nGenerating ID string from data_source + Symbol + Date + Market Category")
    if len(df['Market Category'][0].replace(' ', '')) > 0:
        print(len(df['Market Category'][0].replace(' ', '')))
        df['ID'] = (data_source.lower() + df['Symbol'] + 
            df['Date'].str.replace('-', '').str.replace('_', '') + df['Market Category'].str.replace(' ', '').str.lower())
    else:
        df['ID'] = (data_source.lower() + df['Symbol'] + 
            df['Date'].str.replace('-', '').str.replace('_', '') + df['Market'].str.replace(' ', '').str.lower())

    # drop the unecessary pandas index (which doesn't get inserted to duckdb)
    df.reset_index(drop=True, inplace=True)

    # Check for null values in the ID column
    null_ids = df['ID'].isnull()
    if null_ids.any():
        print("Null values found in ID column:")
        print(df[null_ids])

    return df
    

def load_df_to_duckdb(df, db_path, data_source):
    '''
        loads df into duckdb by running clean_df() and asserting a table with the proper schema
    ''' 

    # Easily change the table naming convention
    table_name = data_source.lower() + '_regsho_daily'

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    # Unify field names (renaming, drop columns, reset index)
    df = clean_df(df=df, data_source=data_source)

    print(f"Inserting cleaned dataframe: {df.head(3)}")

    con = duckdb.connect(database=db_path, read_only=False)
    # Ensure the table exists with the correct schema
    try:
        con.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            "ID" VARCHAR PRIMARY KEY,
            "Date" DATE,
            "Symbol" VARCHAR,
            "Security Name" VARCHAR,
            "Market Category" VARCHAR,
            "Market" VARCHAR,
            "Reg SHO Threshold Flag" VARCHAR,
            "Threshold List Flag" VARCHAR,
            "FINRA Rule 4320 Flag" VARCHAR,
            "Rule 3210" VARCHAR,
            "Data Provider" VARCHAR,
            "Source URL" VARCHAR
        )
    """)
    except Exception as e: 
        print(f"\n\n******ERROR******\nCould not make table {table_name} \n {e}\n\n\n\n")
        return None

    # Insert the data into the table
    try: 
        con.execute(f"""
            INSERT INTO {table_name} BY NAME
            SELECT * FROM df
        """)
        print("Inserted df into duckdb table")
    except Exception as e: 
        print(f'\n\n**********ERROR*******\nDB LOAD FAILED {e}\n\n')
    con.close()

    return df



def regsho_by_date(datestring, data_sources, db_path):
    '''
    Grabs records by date for all data sources supplied

    Args:
    data_sources: [List]; One or all of ['nyse', 'nasdaq', 'finra']
    datestring: Str; YYYYmmdd format
    '''

    dfs=[]
    print(data_sources)
    for data_source in data_sources:
        print(f"Pulling data from {data_source} for {datestring}")

        if data_source == 'finra':
            df = finra_by_date(datestring=datestring, db_path=db_path)
        elif data_source == 'cboe':
            try:
                df = cboe_by_date(datestring=datestring, db_path=db_path)
            except Exception as e:
                print(e)
        elif data_source == 'nasdaq':
            df = nasdaq_by_date(datestring=datestring, db_path=db_path)
        elif data_source == 'nyse':
            df = nyse_by_date(datestring=datestring, db_path=db_path)
        else:
            print("\nERROR: No valid data source supplied\n\n")

        if df is not None and not df.empty:
            dfs.append(df)

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    


def regsho_by_range(start_date, end_date, data_sources, db_path):
    '''
    Args:
    start_date: String %Y%m%d aka YYYYmmdd (e.g. 20240125 = jan 25 2024)
    end_date: String %Y%m%d, or 'yesterday'

    Returns: df of values that failed to load into DuckDB
    '''

    # Gather properly formated list of datestrings (e.g. "YYYY_MM_dd"to feed into download url string 
    datestrings = generate_date_strings(start_date, end_date)
    print(f"\n\n\n\n\n\nPulling data for dates ranging: {start_date}-{end_date}")
    dfs = []
    for datestring in datestrings:
        # Download file
        try: 
            print(f"\n\n\nDownloading data for date: {datestring}")
            df = regsho_by_date(datestring=datestring, data_sources=data_sources, db_path=db_path)
            if not df.empty:
                dfs.append(df)
            # Concatenate all DataFrames into a single DataFrame
            # final_df = pd.concat(dfs, ignore_index=True)
        except Exception as e:
            print(f"\n\n\nCould not grab data for date: {datestring} -- This was probably a holiday/non-trading day -- skipping to next day\n********************\n\n")

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()


def pull_all(data_sources, start_date, end_date='yesterday', db_path='./stonk.duckdb'):
    ''' should save data to duckdb file or return failed rows as a df. If the df is empty, all data that was retreived was loaded '''

    print(f"Attempting to download requested data from: {list(data_sources)}.\n It will try to load the records by date from each source into their own DuckDB tables, then combine them. \
    \n Any data that fails to be loaded will return as a dataframe. Any request that fails will skip to the next date.")
    df = pd.DataFrame()
    df = regsho_by_range(start_date=start_date, end_date=end_date, data_sources=data_sources, db_path='./stonk.duckdb')
    if not df.empty:
        print("Some rows were not added to duckdb")
        print(df)
    else:
        print("\n\n\nNo dataframe returned, meaning that all data that was successfully retrieved was successfully loaded into database. This does not yet indicate failures to actually retrieve the data, it currently just skips to the next date.\n")

    return df



def merge_tables(db_path='./stonk.duckdb'):
    con = duckdb.connect(database=db_path, read_only=False)
    # Check if the table exists
    table_exists = con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'regsho_daily'").fetchone()[0] > 0
    
    if table_exists:
        # Drop the existing table
        con.execute("DROP TABLE regsho_daily")

    con.execute(f"""
            CREATE TABLE regsho_daily AS
            SELECT * FROM nasdaq_regsho_daily
            UNION ALL
            SELECT * FROM nyse_regsho_daily
            UNION ALL
            SELECT * FROM finra_regsho_daily
            UNION ALL
            SELECT * FROM cboe_regsho_daily
            ORDER BY Date;
        """)
    con.close()
    return print("Merging tables...")



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

