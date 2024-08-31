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

    
    


def main(start_date: str, end_date: str, data_sources):
    '''
    Grabs records by date for all data sources supplied

    Args:
    data_sources: [List]; One or all of ['nyse', 'nasdaq', 'finra']
    start_date/end_date; YYYYmmdd format
    '''

    dfs=[]
    for data_source in data_sources:
        table_name = 'regsho_daily'          # Easily change the table naming convention
        print(f"\n\n**** Pulling data from {data_source} for {datestring}")
        try:
            if data_source == 'finra':
                df = finra(start_date=start_date, end_date=end_date)
            elif data_source == 'cboe':
                df = cboe(start_date=start_date, end_date=end_date)
            elif data_source == 'nasdaq':
                df = nasdaq(start_date=start_date, end_date=end_date)
            elif data_source == 'nyse':
                df = nyse(start_date=start_date, end_date=end_date)
            else:
                print("\nERROR: No valid data source supplied\n\n")
                return
        except:
            continue

   


def cboe(start_date='20240101', end_date='today'):
    datestrings = generate_datestrings(start_date='20240101', end_date='today')
    urls = [f'https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/{datestring}/csv' for f'{datestring[:4]}-{datestring[4:6]}-{datestring[6:8]}' in datestrings]

    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=clean_df
    )




def finra(datareq_type='data', group='otcmarket', dataset='thresholdlist', datestring='20240704', limit=1000) -> Optional[Union[List[dict], List]]:
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

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    params = {  # This part allows date filtering
        "limit": limit,
        "offset": offset,
        "compareFilters": [{ "fieldName": "tradeDate", "compareType": "equal", "fieldValue": datestring}]
    }

    if not token:
        print("\nToken for FINRA API could not be generated.")
        return

    datestring = f'{datestring[:4]}-{datestring[4:6]}-{datestring[6:8]}' # this is faster than datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
    urls=[]
    for datestring in datestrings:
        urls.append(f"https://api.finra.org/{datareq_type}/group/{group}/name/{dataset}")
   
    # response = requests.post(url, headers=headers, json=params)     # Note: the request type must be POST for filtering the query
    datestrings = generate_datestrings(start_date='20240101', end_date='today')
    urls = gen_urls(datestrings)
    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=clean_df,
        params=params
    )




def nasdaq(start_date:str='20240101', end_date:str='today'):
    ''' datestring must be in format YYYYmmdd '''

    datestrings = generate_datestrings(start_date='20240101', end_date='today')
    
    urls = [f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{date}.txt' for date in datestrings]

    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        market='Nasdaq',
        chunk_size=100000,
        transform_func=clean_df
    )




def nyse(start_date='20240101', end_date='today'):
    '''
        Grabs reg sho threshold list data from all NYSE markets (.self, American, and Arca)

        Args:
        start_date/end_date: the date range you want data for. YYYYmmdd
        markets: List of NYSE markets to search; any combination of ['NYSE', 'NYSE%20Arca', 'NYSE%20American']
    '''
    if not markets:
        markets = ['NYSE', 'NYSE%20Arca', 'NYSE%20American']
        print("Setting markets to pull from:", markets)
    # NYSE has 3 Exchanges/TRFs that report FTDs: NYSE, NYSE American, and NYSE Arca
    # This collects records from all of them 
    datestrings = generate_datestrings(start_date=20240101, end_date='today')
    urls=[]
    
    for datestring in datestrings:
        for market in markets:
            date_format = '%d-%b-%Y'    # Format that the url query string expects
            date = datetime.strptime(datestring, '%Y%m%d').strftime(date_format)
            urls.append(f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={date}&market={market}')


    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=clean_df,
        market = market
    )
               
        



def clean_df(df: pd.DataFrame, url: str, data_source='NYSE', market:str) -> pd.DataFrame:
    '''
    Field definitions:  
    Nasdaq: https://www.nasdaqtrader.com/Trader.aspx?id=RegShoDefs
    NYSE: follows the same schema :) (also I can't find a data dict for it)
    FINRA: https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock
    '''

    df = df.iloc[:-1]   # Remove the last line which is only datestring
    df['Source URL'] = url
    df['Market'] = market.replace('%20', ' ')
    # df['Date'] = pd.to_datetime(datestring, format='%Y%m%d') #.strptime('%Y-%m-%d').   

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

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)   # Remove spaces to the right and left of all values

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