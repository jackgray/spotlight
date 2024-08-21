'''
Development area for data retreival and cleaning. To be replaced by api.py + producer.py, etc

'''

import requests
import backoff
from zipfile import ZipFile
import os
from os import listdir, path, remove, makedirs, getenv
import csv
import duckdb
import pandas as pd
import polars as pl
from datetime import datetime, timedelta
from glob import glob
from io import BytesIO, TextIOWrapper
from typing import Optional, Required, List, Union
from clickhouse_connect import get_client as ch

# from config import schema


local_run = True

table_name = 'sec_swaps_dtcc1'


sourcedata_path = f'../data/sourcedata'
rawdata_path = f'../data/rawdata'

swaps_dir = f'{sourcedata_path}/swaps'

if local_run:
    # Define file location and output path
    output_path = '../data/sourcedata/swaps' #path to folder where you want filtered reports to save

    os.makedirs(sourcedata_path, exist_ok=True)
    os.makedirs(rawdata_path, exist_ok=True)


# Note that SEC data does not contain Foreign exchange (FOREX) or interest swap reports
jurisdictions = ['SEC', 'CFTC']
report_types = ['SLICE', 'CUMULATIVE', 'FOREX', 'INTEREST' ]
asset_classes = ['CREDITS', 'EQUITIES', 'RATES']


def download_batch(start_date, end_date, table_name, schema_dict, ch_settings):
    '''
    Downloads SEC Swap data files for a range of dates

    Depends on: generate_date_strings(), download_and_unzip()

    Args:
    start_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)
    end_date: String
    '''

    # Gather properly formated list of datestrings (e.g. "YYYY_MM_dd"to feed into download url string 
    datestrings = generate_date_strings(start_date, end_date)
    print(f"Pulling data for the following dates: {list(datestrings)}")
    for datestring in datestrings:
        # Download file
        url = gen_url('SEC', 'CUMULATIVE', 'EQUITIES', datestring)
        print(f"Retrieving {url}")
        df = fetch_zip_to_memory(url)
        
        print(df.dtypes)
        print(df.head(3))
        print("Inserting data to clickhouse db")

        # csv_to_clickhouse(headers= data=data, table_name=table_name, schema_dict=schema_dict, ch_settings=ch_settings )


def fetch_zip_to_memory(url):
    res = backoff_fetch(url)

    with ZipFile(BytesIO(res.content)) as zipref:
        csv_filename = zipref.namelist()[0]
        with zipref.open(csv_filename) as csv_file:
            reader = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
            with zipref.open(csv_filename) as csv_file:
                df = pd.read_csv(csv_file)
            data = []

            # field_indices = {field: headers.index(field) for field in schema_dict}
            df.replace('', pd.NA, inplace=True)
            for field, expected_type in schema_dict.items():
                if field in df.columns:
                    if 'DateTime' in expected_type:
                        df[field] = pd.to_datetime(df[field], errors='coerce')
                    elif 'Int' in expected_type:
                        df[field] = pd.to_numeric(df[field], errors='coerce').astype('Int64')
                    elif 'Float' in expected_type:
                        df[field] = pd.to_numeric(df[field], errors='coerce').astype('float64')
                    elif 'String' in expected_type:
                        df[field] = df[field].astype(str).replace('nan', pd.NA).replace(' ', '_')
                    else:
                        # Handle other data types as needed
                        pass

                    # Check for any NaT or NaN values indicating type conversion failure
                    if df[field].isna().any():
                        print(f"Type mismatch in field '{field}': expected {expected_type}, but some values could not be converted")

    print(f'\nData collected has {df.shape[1]} columns')
    return df
            
            
def csv_to_clickhouse(headers, data, schema_dict, table_name, ch_settings):  
        
    ch_conn = ch(**ch_settings)

    columns = [col.replace(' ', '_').replace('-','_').replace('/', '_') for col in list(schema_dict.keys())]
    # Prepare the column definitions for the CREATE TABLE statement
    columns_sql = ', '.join([f"""{col.replace(' ', '_').replace('-','_').replace('/','_')} {dtype}""" for col, dtype in schema_dict.items()])


    print("Schema columns:", columns)
    print("Data columns:", headers) 
    # Create the table if it doesn't exist
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_sql}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """
    if len(headers) != len(columns):
        print("\nSchema mismatch")
        return

    print(f"\n\nCreating table with {len(columns)} headers: ", columns_sql)
    ch_conn.command(create_table_sql)

    # ClickHouse expects the values to be a flattened list for bulk insert
    flattened_data = [item for sublist in data for item in sublist]

    print(f"\nInserting {len(headers)} data of len: ", len(data))
    print(f"which should fit schema of {len(columns)} columns")
    
    # Insert data in one query if data is available
    if data:
        print(headers)
        # for row in data:
        #     print(f"len of row: {len(row)}")
        #     print(f"row: ", tuple(row))
        #     # for i in row:
        #     #     print(i)
        #     # print(f"\ninserting row {row}")
        ch_conn.insert(table_name, data, column_names=columns)



# Function to assert the type of a value
def assert_type(value, expected_type):
    if expected_type.startswith('Nullable'):
        if value == '' or value is None:
            return True
        expected_type = expected_type[len('Nullable('):-1]

    if expected_type == 'String':
        return isinstance(value, str)
    elif expected_type == 'Float64':
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif expected_type == 'Int64':
        try:
            int(value)
            return True
        except ValueError:
            return False
    elif expected_type == 'Date':
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    elif expected_type == 'DateTime64':
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    else:
        return False

def generate_pandas_schema(schema_dict):
    '''
        Convert ClickHouse schema to pandas to assert types before insert. Because ClickHouse does not seem to support type casting in connect inserts.
    '''
    type_mapping = {
        'String': 'object',
        'Nullable(String)': 'object',
        'Date': 'datetime64[ns]',
        'Nullable(Date)': 'datetime64[ns]'
    }
    
    pandas_schema = {}
    for column_name, column_type in schema_dict.items():
        pandas_schema[column_name] = type_mapping.get(column_type, 'object')  # default to 'object' for unknown types

    return pandas_schema

def clean_numeric_string(value):
    """Remove commas from numeric strings and convert to float."""
    # if value == '':
    #     return None  # Replace null values with an empty string
    
    if isinstance(value, str):
        value = value.replace(',', '').replace(':','').replace('-','')
    try:
        return str(value)
    except ValueError:
        return value

def process_csv_data_in_memory(csv_data):
    """Clean numeric values from in-memory CSV data."""
    # Use StringIO to treat the string as a file
    csv_file = io.StringIO(csv_data)
    reader = csv.reader(csv_file)
    
    # Read header
    headers = next(reader)
    
    # Process rows
    cleaned_data = []
    for row in reader:
        cleaned_row = [clean_numeric_string(cell) for cell in row]
        cleaned_data.append(cleaned_row)
    
    return  cleaned_data



def generate_date_strings(start_date = '20190101', end_date='today') -> Required[str]:
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



def gen_url(jurisdiction, report_type, asset_class, datestring):
    datestr_fmt = f'{datestring[:4]}_{datestring[4:6]}_{datestring[6:8]}'
    dtcc_url = 'https://pddata.dtcc.com/ppd/api/report'
    return f'{dtcc_url}/{report_type.lower()}/{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestr_fmt}.zip'


@backoff.on_exception(
    backoff.expo,  # Exponential backoff
    requests.exceptions.RequestException,  # Retry on any request exception
    max_tries=1  # Number of retries before giving up
)
def backoff_fetch(url):
    res = requests.get(url.strip(), stream=True)
    res.raise_for_status()
    return res




date_fields = [
    'Effective Date',
    'Expiration Date',
    'Maturity date of the underlier',
    'Effective date of the notional amount-Leg 1',
    'Effective date of the notional amount-Leg 2',
    'End date of the notional amount-Leg 1',
    'End date of the notional amount-Leg 2',
    'First exercise date'
]

price_fields = [
    'Call amount',
    'Put amount',
    'Exchange rate',
    'Fixed rate-Leg 1',
    'Fixed rate-Leg 2',
    'Option Premium Amount',
    'Price',
    'Spread-Leg 1',
    'Spread-Leg 2',
    'Strike Price',
    'Package transaction price',
    'Package transaction spread',
    'Index factor'
]


ch_settings = {
    'host': '192.168.8.246',
    'port': 8123,
    'database': 'default',
    'username': 'default',
    'password': ''}

schema_dict = {
    'Dissemination Identifier': 'String',
    'Original Dissemination Identifier': 'Nullable(String)',
    'Action type': 'Nullable(String)',
    'Event type': 'Nullable(String)',
    'Event timestamp': 'Nullable(DateTime64)',
    'Amendment indicator': 'Nullable(String)',
    'Asset Class': 'Nullable(String)',
    'Product name': 'Nullable(String)',
    'Cleared': 'Nullable(String)',
    'Mandatory clearing indicator': 'Nullable(String)',
    'Execution Timestamp': 'Nullable(DateTime64)',
    'Effective Date': 'Nullable(Date)',
    'Expiration Date': 'Nullable(Date)',
    'Maturity date of the underlier': 'Nullable(Date)',
    'Non-standardized term indicator': 'Nullable(String)',
    'Platform identifier': 'Nullable(String)',
    'Prime brokerage transaction indicator': 'Nullable(String)',
    'Block trade election indicator': 'Nullable(String)',
    'Large notional off-facility swap election indicator': 'Nullable(String)',
    'Notional amount-Leg 1': 'Nullable(Float64)',
    'Notional amount-Leg 2': 'Nullable(Float64)',
    'Notional currency-Leg 1': 'Nullable(String)',
    'Notional currency-Leg 2': 'Nullable(String)',
    'Notional quantity-Leg 1': 'Nullable(String)',
    'Notional quantity-Leg 2': 'Nullable(String)',
    'Total notional quantity-Leg 1': 'Nullable(String)',
    'Total notional quantity-Leg 2': 'Nullable(String)',
    'Quantity frequency multiplier-Leg 1': 'Nullable(String)',
    'Quantity frequency multiplier-Leg 2': 'Nullable(String)',
    'Quantity unit of measure-Leg 1': 'Nullable(String)',
    'Quantity unit of measure-Leg 2': 'Nullable(String)',
    'Quantity frequency-Leg 1': 'Nullable(String)',
    'Quantity frequency-Leg 2': 'Nullable(String)',
    'Notional amount in effect on associated effective date-Leg 1': 'Nullable(String)',
    'Notional amount in effect on associated effective date-Leg 2': 'Nullable(String)',
    'Effective date of the notional amount-Leg 1': 'Nullable(Date)',
    'Effective date of the notional amount-Leg 2': 'Nullable(Date)',
    'End date of the notional amount-Leg 1': 'Nullable(Date)',
    'End date of the notional amount-Leg 2': 'Nullable(Date)',
    'Call amount': 'Nullable(String)',
    'Call currency': 'Nullable(String)',
    'Put amount': 'Nullable(String)',
    'Put currency': 'Nullable(String)',
    'Exchange rate': 'Nullable(String)',
    'Exchange rate basis': 'Nullable(String)',
    'First exercise date': 'Nullable(Date)',
    'Fixed rate-Leg 1': 'Nullable(String)',
    'Fixed rate-Leg 2': 'Nullable(String)',
    'Option Premium Amount': 'Nullable(String)',
    'Option Premium Currency': 'Nullable(String)',
    'Price': 'Nullable(Float64)',
    'Price unit of measure': 'Nullable(String)',
    'Spread-Leg 1': 'Nullable(String)',
    'Spread-Leg 2': 'Nullable(String)',
    'Spread currency-Leg 1': 'Nullable(String)',
    'Spread currency-Leg 2': 'Nullable(String)',
    'Strike Price': 'Nullable(Float64)',
    'Strike price currency/currency pair': 'Nullable(Float64)',
    'Post-priced swap indicator': 'Nullable(String)',
    'Price currency': 'Nullable(String)',
    'Price notation': 'Nullable(String)',
    'Spread notation-Leg 1': 'Nullable(String)',
    'Spread notation-Leg 2': 'Nullable(String)',
    'Strike price notation': 'Nullable(Float64)',
    'Fixed rate day count convention-leg 1': 'Nullable(Int64)',
    'Fixed rate day count convention-leg 2': 'Nullable(Int64)',
    'Floating rate day count convention-leg 1': 'Nullable(Int64)',
    'Floating rate day count convention-leg 2': 'Nullable(Int64)',
    'Floating rate reset frequency period-leg 1': 'Nullable(Int64)',
    'Floating rate reset frequency period-leg 2': 'Nullable(Int64)',
    'Floating rate reset frequency period multiplier-leg 1': 'Nullable(String)',
    'Floating rate reset frequency period multiplier-leg 2': 'Nullable(String)',
    'Other payment amount': 'Nullable(String)',
    'Fixed rate payment frequency period-Leg 1': 'Nullable(String)',
    'Floating rate payment frequency period-Leg 1': 'Nullable(String)',
    'Fixed rate payment frequency period-Leg 2': 'Nullable(String)',
    'Floating rate payment frequency period-Leg 2': 'Nullable(String)',
    'Fixed rate payment frequency period multiplier-Leg 1': 'Nullable(String)',
    'Floating rate payment frequency period multiplier-Leg 1': 'Nullable(String)',
    'Fixed rate payment frequency period multiplier-Leg 2': 'Nullable(String)',
    'Floating rate payment frequency period multiplier-Leg 2': 'Nullable(String)',
    'Other payment type': 'Nullable(String)',
    'Other payment currency': 'Nullable(String)',
    'Settlement currency-Leg 1': 'Nullable(String)',
    'Settlement currency-Leg 2': 'Nullable(String)',
    'Settlement location': 'Nullable(String)',
    'Collateralisation category': 'Nullable(String)',
    'Custom basket indicator': 'Nullable(String)',
    'Index factor': 'Nullable(String)',
    'Underlier ID-Leg 1': 'Nullable(String)',
    'Underlier ID-Leg 2': 'Nullable(String)',
    'Underlier ID source-Leg 1': 'Nullable(String)',
    'Underlying Asset Name': 'Nullable(String)',
    'Underlying asset subtype or underlying contract subtype-Leg 1': 'Nullable(String)',
    'Underlying asset subtype or underlying contract subtype-Leg 2': 'Nullable(String)',
    'Embedded Option type': 'Nullable(String)',
    'Option Type': 'Nullable(String)',
    'Option Style': 'Nullable(String)',
    'Package indicator': 'Nullable(String)',
    'Package transaction price': 'Nullable(Float64)',
    'Package transaction price currency': 'Nullable(String)',
    'Package transaction price notation': 'Nullable(String)',
    'Package transaction spread': 'Nullable(String)',
    'Package transaction spread currency': 'Nullable(String)',
    'Package transaction spread notation': 'Nullable(String)',
    'Physical delivery location-Leg 1': 'Nullable(String)',
    'Delivery Type': 'Nullable(String)',
    'Unique Product Identifier': 'Nullable(String)',
    'UPI FISN': 'Nullable(String)',
    'UPI Underlier Name': 'Nullable(String)'
}



# process_ice_data(swaps_dir, 'ICE_swaps')

download_batch('20240201', 'today', table_name='newnew', schema_dict=schema_dict, ch_settings=ch_settings)
