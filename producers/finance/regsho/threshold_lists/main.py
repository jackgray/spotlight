from datetime import datetime, timedelta
import requests
import re
import pandas as pd
import json
from io import StringIO
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Required, List, Union
import time
from clickhouse_connect import get_client as ch
import re
import argparse
import asyncio
from datetime import datetime

from spotlight_utils.main import get_token, create_table_from_dict, generate_datestrings, fetch_with_adaptive_concurrency
    
    


async def main(
    start_date: Required[str] = 'yesterday', 
    end_date: Required[str] = 'today', 
    data_sources: List[str] = None, 
    table_name: Required[str] = 'regsho_daily_source'):

    '''
    Grabs records by date for all data sources supplied

    Args:
    data_sources: [List]; One or all of ['nyse', 'nasdaq', 'finra']
    start_date/end_date; YYYYmmdd format
    '''

    # if data_sources is None:
    #     data_sources = ['cboe', 'finra', 'nasdaq', 'nyse']
    data_sources=['nasdaq']

    dfs=[]
    for data_source in data_sources:
        print("Collecting data from ", data_source)
        try:
            if data_source == 'finra':
                await finra(start_date=start_date, end_date=end_date, table_name=table_name+'_finra')
            elif data_source == 'cboe':
                await cboe(start_date=start_date, end_date=end_date, table_name=table_name+'_cboe')
            elif data_source == 'nasdaq':
                # create_table_from_dict(schema_dict=nasdaq_schema, table_name=table_name+'_nasdaq')
                await nasdaq(start_date=start_date, end_date=end_date, table_name=table_name+'_nasdaq')
            elif data_source == 'nyse':
                await nyse(start_date=start_date, end_date=end_date, table_name=table_name+'_nyse')
            else:
                print("\nERROR: No valid data source supplied\n\n")
                return
        except Exception as e:
            print(e)

   


async def cboe(
    table_name: Required[str], 
    start_date: Required[str] = 'yesterday', 
    end_date: Required[str] = 'today'
    ):

    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    urls = [f'https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/{datestring}/csv' 
        for datestring in [f'{ds[:4]}-{ds[4:6]}-{ds[6:8]}' for ds in datestrings]]

    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=None,
        market='OTC',
        data_source='Cboe'
    )




async def finra(
    table_name: Required[str],
    datareq_type: Required[str] = 'data', 
    group: Required[str] = 'otcmarket', 
    dataset: Required[str] = 'thresholdlist', 
    start_date: Required[str] = 'yesterday',
    end_date: Required[str] = 'today',
    limit=1000) -> Optional[Union[List[dict], List]]:
    
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
    
    urls = [f"https://api.finra.org/{datareq_type}/group/{group}/name/{dataset}?date={ds[:4]}-{ds[4:6]}-{ds[6:8]}" 
        for ds in datestrings]
   
    # response = requests.post(url, headers=headers, json=params)     # Note: the request type must be POST for filtering the query
    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)

    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=None,
        params=params,
    )




async def nasdaq(
    table_name: Required[str],
    start_date: Required[str] = 'yesterday', 
    end_date: Required[str] = 'today'
    ):

    ''' datestring must be in format YYYYmmdd '''

    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    
    urls = [f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{date}.txt' for date in datestrings]

    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=transform_df,
    )




async def nyse(
    table_name: Required[str],
    start_date: Required = 'yesterday', 
    end_date: Required = 'today',
    markets: Required[list] = ['NYSE', 'NYSE%20Arca', 'NYSE%20American']
    ):

    '''
        Grabs reg sho threshold list data from all NYSE markets (.self, American, and Arca)

        Args:
        start_date/end_date: the date range you want data for. YYYYmmdd
        markets: List of NYSE markets to search; any combination of ['NYSE', 'NYSE%20Arca', 'NYSE%20American']
    '''

    # NYSE has 3 Exchanges/TRFs that report FTDs: NYSE, NYSE American, and NYSE Arca
    # This collects records from all of them 
    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    print(datestrings)
    for market in markets:
        # Generate the list of URLs for the current market
        urls = [
            f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={datetime.strptime(datestring, "%Y%m%d").strftime("%d-%b-%Y")}&market={market}' 
            for datestring in datestrings
        ]

        # Fetch data with adaptive concurrency
        await fetch_with_adaptive_concurrency(
            urls=urls,
            table_name=table_name,
            chunk_size=100000,
            transform_func=transform_df,
        )
               
        
def transform_df(df: pd.DataFrame, url: Required[str]):
    print('\n\n\n\n\n\n\n\n\n\n')
    df = df.iloc[:-1]   # Remove the last line which is only datestring
    if len(df) < 3:
        return
    
    df['col1'] = df['col1'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x)))


    df['Source_Url'] = url
    # df.drop(columns='Security Name')
    # df2['Security_Symbol'] = df['Symbol']

    # gen_id = df[]
    df = df.applymap(lambda x: x.replace(', ', '').replace('(', '').replace('.','').replace('$','') if isinstance(x, str) else x)   # Remove invalid characters


    return df


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and process CSV data from ICE US SDR.")
    parser.add_argument('--start_date', type=str, default='20240101', help='Start date in YYYYMMDD format')
    parser.add_argument('--end_date', type=str, default='today', help='End date in YYYYMMDD format (or "today")')
    parser.add_argument('--table_name', type=str, default='regsho_daily_source', help='Table name for ClickHouse')
    parser.add_argument('--data_sources', nargs='+', type=str, default=None, help='List of providers to request from. You may want to consider separating them into batches or single source per run. Must be input as a list inside []')

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(start_date=args.start_date, end_date=args.end_date, table_name=args.table_name))

