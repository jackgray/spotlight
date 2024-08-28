import pandas as pd
from datetime import datetime, timedelta
import json
import duckdb
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Required, List, Union
from datetime import datetime
import time
import re
from io import StringIO
import csv
import requests
import time
import backoff
from clickhouse_connect import get_client as ch

from sources import sources


""" ***************************************** """
"""             GET TOKEN                     """
""" ***************************************** """
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=1)
def get_ice_token():
    session = requests.Session()
    url = "https://tradevault.ice.com/tvsec/ticker/webpi/getToken"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
    }
    # Make the initial request to establish a session and get cookies
    response = session.post(url, headers=headers)

    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Failed to obtain the token. Status code: {response.status_code}")
        exit()



""" ***************************************** """
"""              FETCH DATA                   """
""" ***************************************** """
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=1)
def fetch_csv(url, token):
    session = requests.Session()
    # Update headers to include Authorization if required
    session.headers.update({
        "Authorization": f"Bearer {token}"
    })
    res = session.get(url.strip(), stream=True)
    res.raise_for_status()
    response = session.get(url)
    if res.status_code == 200:
        data = StringIO(response.text)
        csvreader = csv.reader(data)
        # nested = [row for row in csvreader]
        df = pd.read_csv(data, sep=',')                
        return df
    else:
        return None



""" ***************************************** """
"""         MINIMAL CLEANUP (Source)          """
""" ***************************************** """
def prep_origin_df(df, url, datestring):
    ''' Get complete original data into source db with as little change as possible '''
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('_-_','_').str.replace('-','_').str.replace('/','_')  # Remove spaces from column names
    df = df.astype(str)
    df.replace('nan', None, inplace=True)
    df['Report_Date'] = datestring
    df['Source_URL'] = url
    return df


""" ***************************************** """
"""              MAKE TABLE                   """
""" ***************************************** """
def create_table_from_dict(schema_dict, table_name, ch_settings):
    ''' Makes a CH table from a python dict defining column names and their types '''
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])
    columns_str = ", ".join([f"`{col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {coltype}" for col, coltype in schema_dict.items()])  # Flattens col names and their types to SQL query string
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY (Event_timestamp);
    """
    print("\nRunning query: \n", create_table_query)
    ch_conn.command(create_table_query)


""" ***************************************** """
"""              INSERT DF                    """
""" ***************************************** """
def df_to_clickhouse(df, table_name, ch_settings):
    print(f"\nConnecting to {ch_settings['host']} table: {table_name} with settings\n{ch_settings}")
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    print("\n\nInserting from df: ", df)
    ch_conn.insert_df(table_name, df)
    print("\nSuccessfully inserted df")

""" ***************************************** """
"""              STAGING                      """
""" ***************************************** """
def col_txfm(col):
    ''' Converts dashes slashes and spaces to underscores and all words capitalized '''
    return '_'.join([part.capitalize() for part in col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_').split('_')])

def ch_typecast(og_table, new_table, ch_settings, desired_schema):
    ''' Creates new table with proper schema using staging table with all string types '''
    
    print(f"\nConnecting to {ch_settings['host']} with settings\n{ch_settings}")
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    current_schema_query = f"DESCRIBE TABLE {og_table}" 
    current_schema = ch_conn.query(current_schema_query).result_rows    # Gets the current schema
    current_schema_dict = {row[0]: row[1] for row in current_schema}    # Creates a dict from the current schema
    print('\n current schema:\n', current_schema_dict)

    # Use second stage schema to make new table with proper typecasts
    columns_str = ", ".join([f"`{col_txfm(col_name)}` {col_type}" for col_name, col_type in desired_schema.items()])
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {new_table} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """

    print("\nRunning query: \n ", create_table_query)
    ch_conn.command(create_table_query)

    print("\nSuccessfully created table")
    # Modify the copy data query to include the necessary transformation
    select_columns = []
    for col_name, col_type in current_schema_dict.items():
        print(col_name)
        # col_name = col_txfm(col_name)
        if 'timestamp' in col_name:
            print("\n\n\n\n\n",col_name)
            select_columns.append(f"toDateTime64(replace(`{col_name}`, 'Z', ''), 3) AS `{col_name}`")
        else:
            select_columns.append(f"`{col_name}`")

    copy_data_query = f"""
        INSERT INTO {new_table} ({", ".join([f"{col_txfm(col)}" for col in desired_schema.keys()])})
        SELECT {", ".join(select_columns)} FROM {og_table}
    """
    print("\nRunning copy query: ", copy_data_query)
    ch_conn.command(copy_data_query)
    print("\nSuccess")



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
"""                BATCH                      """
""" ***************************************** """
def download_batch(start_date, end_date, table_name, schema_dict, ch_settings):
    '''start/end_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)'''
    token = get_ice_token()
    datestrings = generate_date_strings(start_date, end_date)
    print(f"Pulling data for the following dates: {list(datestrings)}")
    for datestring in datestrings:  
        try:
            ice_by_date(datestring, table_name, token, ch_settings, schema_dict)
            print("Inserting data to clickhouse db")
        except Exception as e:
            print(e)


""" ***************************************** """
"""              SINGLE DATE                  """
""" ***************************************** """
def ice_by_date(datestring, table_name, token, ch_settings, schema_dict):
    url_datestring = '-'.join([datestring[:4], datestring[4:6], datestring[6:8]])
    url = f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={url_datestring}'
    print(f"Retrieving {url}")
    df = fetch_csv(url=url, token=token)
    origin_df = prep_origin_df(df=df, url=url, datestring=url_datestring)   # Staging df
    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, settings=ch_settings)   # Create staging table
    df_to_clickhouse(df=origin_df, table_name=table_name, settings=ch_settings) # Load staging df to staging table



""" ***************************************** """
"""           UNUSED FUNCTIONS                """
""" ***************************************** """
def prep_origin_list(table_name, rows, url, datestring, schema_dict, settings):
    '''Expects rows to be a list of lists, which are each a row'''
    flattened_values = tuple(item for row in rows for item in row)
    num_columns = len(rows[0])
    placeholders = ', '.join(['%s'] * num_columns)
    values_placeholders = ', '.join([f'({placeholders})'] * len(rows))

    # Generate VALUES string
    values = ', '.join(
        f"""({', '.join(['NULL' if value == '' else f"'{value.replace('(','').replace(')','')}'"
                for value in row])})"""
        for row in rows[1:]
    )

    columns = ", ".join([f"`{col_name.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {col_type}" for col_name, col_type in schema_dict.items()])

    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])
    
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """
    print("\nRunning query: \n ", create_table_query)
    ch_conn.command(create_table_query)

    insert_query = f"""
            INSERT INTO {table_name} ({columns}) VALUES {values}
        """
    print("\nRunning insert query: ", insert_query)
    ch_conn.command(insert_query)


def create_table_from_df(df, table_name, schema_dict, settings):
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
        elif "bool" in str(dtype):
            ch_type = "Bool"
        else:
            ch_type = "String"  # Default to String for other types
        columns.append(f"`{col_name}` {ch_type}")
    print("Generated schema: ", columns)            # Skipping schema generation on first load to ensure all data is inserted
    # columns_str = ", ".join(columns)

    columns_str = ", ".join([f"'{col}' {coltype}" for col, coltype in schema_dict.items()])
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """
    print("\nRunning query: \n", create_table_query)
    ch_conn.command(create_table_query)
    print("\nTable created")


