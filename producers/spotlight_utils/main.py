import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Required, List, Union, Callable, Dict
import time
from io import StringIO, BytesIO
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
# For passing a downstream function as argument to these functions (like one to transform data while transferring it asychronously)
TransformFunc = Callable[[pd.DataFrame, str], pd.DataFrame]  # function to transform df mid-stream



""" ***************************************** """
"""             GET TOKEN             """
""" ***************************************** """
@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=2)
async def get_token(url: str) -> str:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "curl/7.78.0"
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
        sep: Optional[str] = ',',
        table_name: Optional[str] = None,
        market: Optional[str] = None,
        data_source: Optional[str] = None,
        token: Optional[str] = None, 
        chunk_size: int = 100000,
        ch_settings: Optional[dict] = ch_settings,  # Optional parameters should come after non-optional
    ) -> None:

    ''' Handle infinitely many fetches and maximize parallelism based on available resources '''

    print("Fetching table")
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
                    logger.info("processing PDF")
                    await fetch_and_process_pdf(
                        url=url, 
                        transform_func=transform_func,
                        market=market,
                        ch_settings=ch_settings
                    )    
                else:
                    print('\n\nFetching and loading CSV')
                    await fetch_and_load_csv(
                        url=url, token=token, 
                        sep=sep,
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
@backoff.on_exception(backoff.expo, httpx.RequestError, max_tries=1)
async def fetch_and_load_csv(
        url: str, 
        table_name: str, 
        token: Optional[str],
        sep: Optional[str] = ',',  
        transform_func: Optional[TransformFunc] = None,
        chunk_size: int = 100000,
        ch_settings: Optional[dict] = ch_settings,
    ) -> None:

    headers = {"Authorization": f"Bearer {token}"} if token else {
        "User-Agent": "curl/7.78.0",
        "Accept": "text/csv, text/plain, */*"
    }

    async with httpx.AsyncClient() as client:
        try:
            logger.info("Fetching file from URL: %s with headers: %s", url, headers)
            response = await client.get(url.strip(), headers=headers)
            response.raise_for_status()

            # Debugging: Print content type and content
            content_type = response.headers.get('content-type')
            logger.info("Content-Type: %s", content_type)
            logger.info("Response content: %s", response.text[:500])  # Print first 500 chars for brevity

            if content_type in ['text/csv', 'text/plain', 'text/plain;charset=utf-8']:
                buffer = StringIO(response.text)
                chunk_counter = 0
                chunk_iter = pd.read_csv(buffer, sep=sep, chunksize=chunk_size)
                for chunk in chunk_iter:

                    # KAFKA PRODUCER FUNCTION  WILL GO HERE
                    print(chunk)
                    if transform_func:
                        print("Transforming...\n")
                        chunk = transform_func(chunk, url)
                    print("Loading chunk into db: ", chunk)

                    # this will be moved to Kafka consumer
                    await load_chunk_to_clickhouse(chunk, table_name, ch_settings)
                    chunk_counter += len(chunk)
                    logger.info(f"Processed chunk with {len(chunk)} rows")

                logger.info(f"Total rows processed: {chunk_counter}")
            else:
                logger.error("Expected CSV or plain text content but received: %s", content_type)
        except httpx.RequestError as e:
            logger.error("Error fetching data from %s: %s", url, e)
            raise


async def fetch_and_process_pdf(
        url: str,
        transform_func: Optional[TransformFunc],
        market: Optional[str],
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
            await transform_func(data, url, market, data_source)   # Loads in the transform function
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
            try:
                create_table_from_df(df=df, table_name=table_name, key_col=key_col, ch_settings=ch_settings)
                ch_conn.insert_df(table_name, chunk)
            except Exception as e:
                exit()

    print("\nSuccessfully inserted all chunks for this segment")



""" ***************************************** """
"""              GET DATESTRINGS              """
""" ***************************************** """
def generate_datestrings(start_date: Required[str] = 'yesterday', end_date: Required[str] = 'today') -> Required[str]:
    '''
    Generates list of (weekday-only) datestrings to supply to URL build parameters for API call

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
def get_schema(table_name, ch_settings=ch_settings):
    ''' Returns dict of current schema '''
    
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    current_schema_query = f"DESCRIBE TABLE {table_name}" 
    current_schema = ch_conn.query(current_schema_query).result_rows    # Gets the current schema
    current_schema_dict = {row[0]: row[1] for row in current_schema}    # Creates a dict from the current schema
    print('\n current schema:\n', current_schema_dict)
    
    return current_schema_dict



def diff_schema(table1, table2, ch_settings):
    ''' Shows columns in table 1 which are not in table 2, and vice-versa '''
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    table1_unique = ch_conn.command(f"""
            SELECT name
            FROM system.columns
            WHERE (`table` = '{table1}') AND (name NOT IN (
                SELECT name
                FROM system.columns
                WHERE `table` = '{table2}'
            ));
        """
    )
    
    table2_unique = ch_conn.command(f"""
            SELECT name
            FROM system.columns
            WHERE (`table` = '{table2}') AND (name NOT IN (
                SELECT name
                FROM system.columns
                WHERE `table` = '{table1}'
            ));
        """
    )

    return table1_unique, table2_unique


def col_txfm(col):
    ''' Converts dashes slashes and spaces to underscores and all words capitalized '''
    return '_'.join([part for part in col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_').split('_')])



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
    
    columns_str = ", ".join([f"`{col_txfm(col)}` {coltype}" for col, coltype in schema_dict.items()])  # Flattens col names and their types to SQL query string
    
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




def ch_typecast(src_table: str, dst_table: str, schema: Dict[str, str], key_col: str, ch_settings: Dict[str, str]=ch_settings) -> None:
    ''' 
    Copies table with new schema and basic formatting transformations
    Inputs: source table name, target table name, Clickhouse schema as a dict
    '''
    
    print("Creating table using input schema")
    create_table_from_dict(
        schema_dict=schema,
        table_name=dst_table,
        key_col=key_col,
        ch_settings=ch_settings
    )
    print("\nSuccessfully created table")

    '''
        Automatically build query that will transform any timestamp fields into castable format. 
        Transform other columns' SELECT statement by name pattern matching to use clickhouse engine for typecasting on massive tables
    '''
    print("Getting schema of source table")
    src_schema = get_schema(table_name=src_table, ch_settings=ch_settings)
    

    # Modify the copy data query to include the necessary transformation
    select_columns = [] # List of columns to copy in INSERT FROM statement
    for col_name, col_type in src_schema.items():
        print(col_name)
        # col_name = col_txfm(col_name)
        if 'timestamp' in col_name:
            print("\n\n\n\n\n",col_name)
            select_columns.append(f"toDateTime64(replace(`{col_name}`, 'Z', ''), 3) AS `{col_name}`")
        elif 'date' in col_name.lower():
            select_columns.append(f"toDate(`{col_name}`) AS `{col_name}`")
        else:
            select_columns.append(f"`{col_name}`")

    print("Checking if schemas match")
    if len(select_columns) != len(schema.keys()):
        print("\nSource cols: ", select_columns)
        print("\nTarget schema: ", schema.keys)
        exit()

    print("Inserting source table values into new table")
    copy_data_query = f"""
        INSERT INTO {dst_table} ({", ".join([f"{col_txfm(col)}" for col in schema.keys()])})
        SELECT {", ".join(select_columns)} FROM {src_table}
    """
    
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])
    print("\nRunning copy query: ", copy_data_query)
    ch_conn.command(copy_data_query)
    print("\nSuccess")

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