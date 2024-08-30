import pandas as pd
from datetime import datetime, timedelta
import json
import duckdb
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Required, List, Union, Callable, Dict
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
import asyncio
import psutil
import logging
import pdfplumber

from spotlight_utils.config import ch_settings
print(ch_settings)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# For passing function as argument to these functions
TransformFunc = Callable[[pd.DataFrame, str], pd.DataFrame]  # function to transform df mid-stream



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
"""              PARALLEL  FETCH              """
""" ***************************************** """
async def fetch_with_adaptive_concurrency(
        urls: List[str], 
        transform_func: Optional[TransformFunc],
        table_name: Optional[str] = None, 
        token: Optional[str] = None, 
        chunk_size: int = 100000,
        ch_settings: Optional[dict] = ch_settings,  # Optional parameters should come after non-optional
    ) -> None:

    ''' Handle infinitely many fetches and maximize parallelism based on available resources '''
    
    def get_concurrency():
        cpu_usage = psutil.cpu_percent(interval=1)  # poll CPU usage
        memory_available = psutil.virtual_memory().available    # poll available memory
        max_concurrency = max(1, min(10, int(memory_available / (1024 * 1024 * 100))))
        if cpu_usage > 75:
            max_concurrency = max(1, max_concurrency // 2)
        return max_concurrency

    max_concurrency = get_concurrency()
    semaphore = asyncio.Semaphore(max_concurrency)
    print(f"Max concurrency set to: {max_concurrency}")

    async def limited_fetch(url: str) -> None:
        try:
            async with semaphore:
                if url.lower().endswith('.zip'):
                    await fetch_and_load_zipped_csv(
                        url=url, ch_settings=ch_settings, 
                        table_name=table_name, 
                        chunk_size=chunk_size, 
                        transform_func=transform_func
                    )
                elif url.lower().endswith('.pdf'):
                    logger.info("processing pdf")
                    await fetch_and_process_pdf(
                        url=url, 
                        transform_func=transform_func,
                        ch_settings=ch_settings
                    )    
                else:
                    await fetch_and_load_csv(
                        url=url, token=token, 
                        ch_settings=ch_settings, 
                        table_name=table_name, 
                        chunk_size=chunk_size, 
                        transform_func=transform_func
                    )
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")

    tasks = [limited_fetch(url=url) for url in urls]    # build jobs list with url passed in arg for downstream use
    await asyncio.gather(*tasks)


""" ***************************************** """
"""              ASYNC FETCH                  """
""" ***************************************** """

@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
async def fetch_and_load_zipped_csv(
        url: str, 
        table_name: str, 
        chunk_size: int = 100000,
        ch_settings: Optional[dict] = None,
        transform_func: Optional[TransformFunc] = None
    ) -> None:
    
    async with httpx.AsyncClient() as client:
        # Fetch the ZIP file
        response = await client.get(url)
        response.raise_for_status()

        # Read the ZIP file content into memory
        with ZipFile(BytesIO(response.content)) as zipref:
            csv_filename = zipref.namelist()[0]  # Get the first file in the ZIP
            with zipref.open(csv_filename) as csv_file:
                reader = pd.read_csv(csv_file, sep=',', chunksize=chunk_size)
                chunk_counter = 0

                # Process each chunk of the CSV file
                for df_chunk in reader:
                    if transform_func:
                        df_chunk = transform_func(df_chunk, url)
                    await load_chunk_to_clickhouse(df_chunk, table_name, ch_settings)
                    chunk_counter += len(df_chunk)

                print(f"\nTotal rows processed: {chunk_counter}")


@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=3)
async def fetch_and_load_csv(
        url: str, 
        table_name: str, 
        token: str,
        transform_func: Optional[TransformFunc],
        chunk_size: int = 100000,
        ch_settings: Optional[dict] = ch_settings,
    ) -> None:

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    logger.info("Fetching CSV from URL: %s with headers: %s", url, headers)
    async with httpx.AsyncClient() as client:

        try:
            response = await client.get(url.strip(), headers=headers)
            response.raise_for_status()

            if response.headers.get('content-type') == 'text/csv':
                buffer = StringIO(response.text)
                chunk_counter=0
                chunk_iter = pd.read_csv(buffer, chunksize=chunk_size)
                for chunk in chunk_iter:
                    if transform_func:
                        chunk = transform_func(chunk, url)
                    await load_chunk_to_clickhouse(chunk, table_name, ch_settings)
                    chunk_counter += len(chunk)
                    logger.info(f"Processed chunk with {len(chunk)} rows")

                logger.info(f"Total rows processed: {chunk_counter}")
            else:
                logger.error("Expected CSV content but received: %s", response.headers.get('content-type'))
        except httpx.RequestError as e:
            # logger.error("Error fetching data from %s: %s", url, e)
            # raise
            pass

async def fetch_and_process_pdf(
        url: str,
        transform_func: Optional[TransformFunc],
        ch_settings: Optional[dict]
    ) -> None:
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        # response.raise_for_status()
        pdf_bytes = BytesIO(response.content)

    
        data = []
        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages[-8:]:
                table = page.extract_table()
                if table is not None:
                    data.append(table)
        if transform_func:
            await transform_func(data, url)   # Loads in the transform function
            logger.info("Successfully loaded report to Clickhouse")
        else:
            logger.error(f"Missing required transform function. Exiting.")
            exit()


""" ***************************************** """
"""              INSERT DF                    """
""" ***************************************** """
async def load_chunk_to_clickhouse(df: pd.DataFrame, table_name: str, ch_settings: Optional[dict], chunk_size: int = 100000) -> None:
    
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



""" ***************************************** """
"""              GET DATESTRINGS              """
""" ***************************************** """
def generate_datestrings(start_date='20190101', end_date='today') -> Required[str]:
    '''
    Generates list of datestrings to supply to URL build parameters for API call

    Dates must be formatted as %Y%m%d aka YYYYmmdd; 'yesterday' and 'today' will generate the datestring based on datetime.now
    '''
    date_format = '%Y%m%d'
    # convert select string inputs to a date representation
    dates = { 'yesterday': (datetime.now() - timedelta(days=1)).strftime(date_format),
                'today': datetime.now().strftime(date_format) }
    start_date = dates.get(start_date, start_date)
    end_date = dates.get(end_date, end_date)

    try:  # Parse the input date strings into datetime objects
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
        if current_date.weekday() < 5:  # only add to list if it is a weekday (monday-friday)
            date_str = current_date.strftime(date_format)   # Format the current date as 'YYYYmmdd'
            date_strings.append(date_str)
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
def create_table_from_dict(
        schema_dict: Dict[str, str],
        table_name: str,
        key_col: str,
        ch_settings: Dict[str, str] = ch_settings
    ) -> None:

    ''' Makes a CH table from a python dict defining column names and their types '''
    
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])
    
    columns_str = ", ".join([f"`{col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {coltype}" 
    for col, coltype in schema_dict.items()])  # Flattens col names and their types to SQL query string
    
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

    logger.info("Running query: \n%s", create_table_query)

    try:
        ch_conn.command(create_table_query)
        logger.info("Table '%s' created successfully.", table_name)
    except Exception as e:
        logger.error("Failed to create table '%s': %s", table_name, e)
        raise  # Re-raise the exception to ensure it's handled by the caller or system


async def create_table_from_df(df: pd.DataFrame, table_name: str, key_col: str, ch_settings: Dict[str, str]=ch_settings) -> None:
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    columns = []
    for col_name, dtype in zip(df.columns, df.dtypes):
        if "int" in str(dtype):
            ch_type = "Int64"
        elif "float" in str(dtype):
            ch_type = "Float64"
        elif "object" in str(dtype):
            ch_type = "String"
        elif "datetime" in str(dtype):
            ch_type = "DateTime"
        else:
            ch_type = "String"  # Default to String for other types
        columns.append(f"`{col_name}` {ch_type}")
    columns_str = ", ".join(columns)
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        PRIMARY KEY ({key_col})
        ORDER BY ({key_col})
        SETTINGS storage_policy = 's3_main';
    """
    ch_conn.command(create_table_query)