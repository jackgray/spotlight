import pandas as pd
from datetime import datetime, timedelta
import json
import duckdb
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Required, List, Union
import time
import re
from io import StringIO, BytesIO
import csv
import requests
import time
import backoff
from clickhouse_connect import get_client as ch
from zipfile import ZipFile

import asyncio
import logging
import httpx
import pandas as pd
from io import StringIO
from typing import List, Optional



""" ***************************************** """
"""             GET TOKEN             """
""" ***************************************** """
@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=1)
async def get_token(url: str) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers)
        response.raise_for_status()  # This will raise an exception for HTTP error codes

        token = response.json().get('token')
        if not token:
            raise ValueError("Token not found in the response")
        return token



""" ***************************************** """
"""              FETCH DATA                   """
""" ***************************************** """
@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
async def fetch_csv(url: str, token: Optional[str] = None) -> Optional[pd.DataFrame]:
    async with httpx.AsyncClient() as client:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = await client.get(url.strip(), headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            data = StringIO(response.text)
            df = pd.read_csv(data, sep=',')
            return df
        else:
            return None




""" ***************************************** """
"""              FETCH ZIP CSV                """
""" ***************************************** """
@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
async def fetch_zipped_csv(url: str) -> Required[pd.DataFrame]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, stream=True)
        response.raise_for_status()
        if response.status_code == 200:
            with ZipFile(BytesIO(response.content)) as zipref:
                csv_filename = zipref.namelist()[0]
                with zipref.open(csv_filename) as csv_file:
                    df = pd.read_csv(csv_file)
                    return df
        else:
            return None


""" ***************************************** """
"""              FETCH PARALLEL               """
""" ***************************************** """

async def fetch_with_adaptive_concurrency(urls: List[str], token: Optional[str] = None, ch_settings: dict, table_name: str, chunk_size: int = 100000) -> List[Optional[pd.DataFrame]]:
    ''' Handle infinitely many fetches and maximize parallelism based on available resources '''
    
    def get_concurrency():
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_available = psutil.virtual_memory().available
        max_concurrency = max(1, min(10, int(memory_available / (1024 * 1024 * 100))))
        if cpu_usage > 75:
            max_concurrency = max(1, max_concurrency // 2)
        return max_concurrency

    async def limited_fetch(url: str):
        max_concurrency = get_concurrency()
        semaphore = asyncio.Semaphore(max_concurrency)
        async with semaphore:
            return await fetch_and_load_csv(url, token, ch_settings, table_name, chunk_size)

    tasks = [limited_fetch(url) for url in urls]
    return await asyncio.gather(*tasks)



@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
async def fetch_and_load_csv(url: str, table_name: str, ch_settings: dict, token: Optional[str] = None, chunk_size: int = 100000):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with client.stream("GET", url.strip(), headers=headers) as response:
            response.raise_for_status()

            # Initialize a StringIO buffer to accumulate the chunks of data
            buffer = StringIO()
            chunk_counter = 0

            async for chunk in response.aiter_text():
                buffer.write(chunk)
                # Check if buffer is large enough to process a chunk
                if buffer.tell() > 1_000_000:  # Adjust this threshold to suit your needs
                    buffer.seek(0)
                    df = pd.read_csv(buffer, sep=',', nrows=chunk_size)
                    await load_chunk_to_clickhouse(df, table_name, ch_settings)
                    chunk_counter += len(df)
                    buffer.seek(0)
                    buffer.truncate(0)

            # Process any remaining data in the buffer
            buffer.seek(0)
            df = pd.read_csv(buffer, sep=',')
            if not df.empty:
                await load_chunk_to_clickhouse(df, table_name, ch_settings)
                chunk_counter += len(df)
            
            print(f"\nTotal rows processed: {chunk_counter}")




""" ***************************************** """
"""              GET DATESTRINGS              """
""" ***************************************** """
def generate_date_strings(start_date='20190101', end_date='today') -> Required[str]:
    '''
    Generates list of datestrings to supply to URL build parameters for API call

    Dates must be formatted as %Y%m%d aka YYYYmmdd; 'yesterday' and 'today' will generate the datestring based on datetime.now
    '''
    date_format = '%Y%m%d'
    dates = { 'yesterday': (datetime.now() - timedelta(days=1)).strftime(date_format),
                'today': datetime.now().strftime(date_format) }
    start_date = dates.get(start_date, start_date)
    end_date = dates.get(end_date, end_date)

    # Parse the input date strings into datetime objects
    try:
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        print(f"Start date input: {start_date}")
        print(f"End date input: {end_date}")
        return []
    # Initialize an empty list to hold the date strings
    date_strings = []    
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




""" ***************************************** """
"""           GET TABLE SCHEMA                """
""" ***************************************** """
def get_current_schema(table_name, ch_settings):
    ''' Returns dict of current schema '''
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    current_schema_query = f"DESCRIBE TABLE {table_name}" 
    current_schema = ch_conn.query(current_schema_query).result_rows    # Gets the current schema
    current_schema_dict = {row[0]: row[1] for row in current_schema}    # Creates a dict from the current schema
    print('\n current schema:\n', current_schema_dict)
    return current_schema_dict





""" ***************************************** """
"""              MAKE TABLE                   """
""" ***************************************** """
def create_table_from_dict(schema_dict, table_name, key_col, ch_settings):
    ''' Makes a CH table from a python dict defining column names and their types '''
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])
    columns_str = ", ".join([f"`{col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {coltype}" for col, coltype in schema_dict.items()])  # Flattens col names and their types to SQL query string
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        PRIMARY KEY ({key_col})
        ORDER BY ({key_col})
        SETTINGS index_granularity='8192',
        async_insert=1,
        storage_policy = 's3_main';
    """
    print("\nRunning query: \n", create_table_query)
    try:
        ch_conn.command(create_table_query)
    except Exception as e:
        print(e)
        exit()





""" ***************************************** """
"""              INSERT DF                    """
""" ***************************************** """
async def load_chunk_to_clickhouse(df: pd.DataFrame, table_name: str, ch_settings: dict, chunk_size: int = 100000):
    print(f"\nConnecting to {ch_settings['host']} table: {table_name} with settings\n{ch_settings}")
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    print("\n\nInserting DataFrame chunk to ClickHouse")
    num_rows = len(df)
    num_chunks = (num_rows // chunk_size) + (1 if num_rows % chunk_size > 0 else 0)

    for i in range(num_chunks):
        chunk = df[i * chunk_size:(i + 1) * chunk_size]
        print(f"Inserting chunk {i+1}/{num_chunks} with {len(chunk)} rows")
        try:
            ch_conn.insert_df(table_name, chunk)
            print(f"Successfully inserted chunk {i+1}/{num_chunks}")
        except Exception as e:
            print(f"Error inserting chunk {i+1}/{num_chunks}: {e}")
            exit()

    print("\nSuccessfully inserted all chunks for this segment")