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
from datetime import datetime
import time
from clickhouse_connect import get_client as ch
import re



def pull_all(data_sources, start_date, ch_settings, end_date='yesterday', db_path='./stonk.duckdb'):
    ''' should save data to duckdb file or return failed rows as a df. If the df is empty, all data that was retreived was loaded '''

    print(f"Attempting to download requested data from: {list(data_sources)}.\n It will try to load the records by date from each source into their own DuckDB tables, then combine them. \
    \n Any data that fails to be loaded will return as a dataframe. Any request that fails will skip to the next date.")
    df = pd.DataFrame()
    df = regsho_by_range(start_date=start_date, end_date=end_date, data_sources=data_sources, ch_settings=ch_settings, db_path='./stonk.duckdb')
    if not df.empty:
        print("Some rows were not added to duckdb")
        print(df)
    else:
        print("\n\n\nNo dataframe returned, meaning that all data that was successfully retrieved was successfully loaded into database. This does not yet indicate failures to actually retrieve the data, it currently just skips to the next date.\n")

    return df


def regsho_by_range(start_date, end_date, data_sources, ch_settings, db_path):
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
        print(f"\n\n\nDownloading data for date: {datestring}")
        df = regsho_by_date(datestring=datestring, data_sources=data_sources, ch_settings=ch_settings, db_path=db_path)
        if not df.empty:
            dfs.append(df)
        # Concatenate all DataFrames into a single DataFrame
        # final_df = pd.concat(dfs, ignore_index=True)

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()



def regsho_by_date(datestring, data_sources, db_path, ch_settings):
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
            df = finra_by_date(datestring=datestring, ch_settings=ch_settings, db_path=db_path)
        elif data_source == 'cboe':
            try:
                df = cboe_by_date(datestring=datestring, ch_settings=ch_settings, db_path=db_path)
            except Exception as e:
                print(e)
        if data_source == 'nasdaq':
            df = nasdaq_by_date(datestring=datestring, ch_settings=ch_settings, db_path=db_path)
        elif data_source == 'nyse':
            df = nyse_by_date(datestring=datestring, ch_settings=ch_settings, db_path=db_path)
        else:
            print("\nERROR: No valid data source supplied\n\n")

        if df is not None and not df.empty:
            dfs.append(df)

    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    


def cboe_by_date(datestring, ch_settings, db_path='./stonk.duckdb', max_retries=5, backoff_factor=1):
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
                    df['Date'] = pd.to_datetime(datestring, format=date_format)
                    print(df.dtypes)
                    df['Source URL'] = url
                except Exception as e: 
                    print("\n\n\n********************\n", e, "\n********************\n\n")                # Lazy solve for problem of duplicate column being created -- come back and find a better fix
                
                # Send to clickhouse
                print(f"Trying to load into clickhouse")
                try:    
                    print(df.head(3))
                    cleaned = clean_df(df=df, data_source='cboe')
                    df_to_clickhouse(df=cleaned, data_source="cboe", settings=ch_settings)  
                    print("Success!")
                except Exception as e:
                    print(e)

                # return errdf  # Return the dataframe if successful

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
    # return errdf



def finra_by_date(ch_settings, datareq_type='data', group='otcmarket', dataset='thresholdlist', datestring='20240704', db_path='./stonk.duckdb', limit=1000) -> Optional[Union[List[dict], List]]:
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
    print(f"Trying to load into clickhouse")
    try:    
        cleaned = clean_df(df=df, data_sourc='finra')
        df_to_clickhouse(df=cleaned, data_source='finra', settings=ch_settings)  
        print("Success!")
    except Exception as e:
        print(e)

    # return errdf


def nyse_by_date(datestring, ch_settings, markets=None, db_path='./stonk.duckdb', max_retries=3, backoff_factor=1):
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
                            df['Date'] = pd.to_datetime(datestring, format='%Y%m%d') #.strptime('%Y-%m-%d').
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

        try:    
            cleaned = clean_df(df=all_data, data_source='nyse')
            df_to_clickhouse(df=cleaned, data_source='nyse', settings=ch_settings)
            print("Success!")
        except Exception as e:
            print(e)

    # return errdf
         

def nasdaq_by_date(datestring, db_path, ch_settings, max_retries=3, backoff_factor=1):
    ''' datestring must be in format YYYYmmdd '''

    date_format = '%Y%m%d'
    try:
        date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
    except:
        print('date error')
    url =f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{date}.txt'

    print(f"Grabbing data from url: {url}")
    retries = 0
    
    # Send request to server using generated URL
    while retries < max_retries:
    
        response = requests.get(url)
        if response.status_code == 200:
            print(f"\nGot successfull response from server.")
            # print(response['Content-Type'])
            try:
                data = StringIO(response.text)
            except: return
            try:
                df = pd.read_csv(data, sep='|')
            except:
                return
            # Remove the last line  which is only datestring
            df = df.iloc[:-1]
            # Add the date as a new column
            if len(df) < 3:
                return
            print(f"Trying to load into clickhouse")
                    # Unify field names (renaming, drop columns, reset index)
            cleaned = clean_df(df=df, data_source='nasdaq')
            print('clean ', cleaned.head(3))
            df_to_clickhouse(df=cleaned, data_source='nasdaq', settings=ch_settings)
            print("Success!")
        
        elif response.status_code == 404:
            print(f"Error 404: Data not found for {datestring}.")
            return None  # Exit if data is not found
        else:
            print(f"Received status code {response.status_code}. Retrying...")
    # except requests.RequestException as e:
    #     print(f"Error fetching data from {url}: {e}")
    retries += 1
    time.sleep(backoff_factor * retries)  # Exponential backoff
    
    print("Max retries reached. Failed to fetch data.")
    # return df



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
    
    drop_cols = [col for col in ['Filler', 'Filler.1'] if col in df.columns]    # NYSE/NASDAQ put in 'Filler' columns but don't use them. Idk why, but we don't need them rn.
    df.drop(drop_cols, axis=1, inplace=True)
    # Remove spaces to the right and left of all values ()
    # df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


    # Generate unique row ID programatically to avoid duplicate insertions
    print("\nGenerating ID string from data_source + Symbol + Date + Market Category")
  
    # # Check for null values in the ID column
    null_ids = df['ID'].isnull()
    if null_ids.any():
        print("Null values found in ID column:")
        print(df[null_ids])

    schema_mapping = {
        "ID": "str",
        "Date": "datetime64[ns]",
        "Symbol": "str",
        "Security_Name": "str",
        "Market Category": "str",
        "Market": "str",
        "Reg SHO Threshold Flag": "str",
        "Threshold List Flag": "str",
        "FINRA Rule 4320 Flag": "str",
        "Rule 3210": "str",
        "Data Provider": "str",
        "Source URL": "str"
    }

    return df  print(df['Date'])
    if len(df['Market Category'][0].replace(' ', '')) > 0:
        print(len(df['Market Category'][0].replace(' ', '')))
        df['ID'] = (data_source.lower() + df['Symbol'] + 
            df['Date'].dt.strftime('%Y%m%d').replace('-', '_') + df['Market Category'].str.replace(' ', '').str.lower())
    else:
        df['ID'] = (data_source.lower() + df['Symbol'].str.replace(' ', '') + 
            df['Date'].dt.strftime('%Y%m%d').replace('-', '') + df['Market'].str.replace(' ', '').str.lower())

    # drop the unecessary pandas index (which doesn't get inserted to duckdb)
    df.reset_index(drop=True, inplace=True)



    
def df_to_clickhouse(df, data_source, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

    # Easily change the table naming convention
    table_name = data_source.lower() + '_regsho_daily'

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    create_table_from_df(df, table_name=table_name, settings=settings)

    ch_conn.insert_df(table_name, df)


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

