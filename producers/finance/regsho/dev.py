'''
Development area for data retreival and cleaning. To be replaced by api.py + producer.py, etc

'''



import requests
from zipfile import ZipFile
import os
from os import listdir, path, remove, makedirs, getenv
import duckdb
import pandas as pd
import polars as pl
from datetime import datetime, timedelta
from glob import glob
from clickhouse_connect import get_client as ch


local_run = True

table_name = 'sec_swaps_dtcc'
# table_name = 'gme_swaps_raw'


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

def gen_url(jurisdiction, report_type, asset_class, datestring):
    dtcc_url = 'https://pddata.dtcc.com/ppd/api/report'
    return f'{dtcc_url}/{report_type.lower()}/{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestring}.zip'


def generate_date_strings(start_date, end_date):
    # Parse the input date strings into datetime objects
    date_format = '%Y%m%d'
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
        # Format the current date as 'year_month_day'
        date_str = current_date.strftime('%Y_%m_%d')
        date_strings.append(date_str)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    return date_strings



def download_and_unzip(url, extract_to=swaps_dir):
    '''
    Unzips files and returns dataframe 
    '''

    # Download the file
    zipfile_name = url.split('/')[-1]
    print('Zipfile: ', zipfile_name)
    with requests.get(url.strip(), stream=True) as r:
        r.raise_for_status()
        with open(zipfile_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # Unzip the file
    with ZipFile(zipfile_name, 'r') as zip_ref:
        csv_filename = zip_ref.namelist()[0]
        zip_ref.extractall(extract_to)

    # Clean up the zip file
    remove(zipfile_name)

    filepath = f'{extract_to}/{csv_filename}'

    # Load content into dataframe
    return pd.read_csv(filepath, low_memory=False)


def cast_columns(df: pd.DataFrame, columns: list, dtype: str) -> pd.DataFrame:
    """
    Cast specified columns in a DataFrame to the given data type.

    Parameters:
    - df: pd.DataFrame - The DataFrame to modify.
    - columns: list - List of column names to cast.
    - dtype: str - Data type to cast the columns to (e.g., 'int', 'float', 'str', 'datetime64').

    Returns:
    - pd.DataFrame - DataFrame with the specified columns cast to the new data type.
    """

    for col in columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                print(f"Error casting column {col} to {dtype}: {e}")

    return df


def clean_df(df):
    # Assert uniformity for changing column labels across data releases (schema drift)

    # column names and Action type labels in the reports changed on 12/04/22 


    # NOTE Polars df.rename cannot gracefully handle a rename map that has fields not contained in df, meaning you would need a different map for each schema
    #   solution here is to use Pandas even though it's slower, its cleaner and easier to read and maintain
    


    column_map = {
        'Dissemination ID': 'Dissemination Identifier',
        'Original Dissemination ID': 'Original Dissemination Identifier',
        'Action Type': 'Action type',
        'Action': 'Action type',
        'Effective Date': 'Effective Date',
        'Expiration Date': 'Expiration Date',
        'Event Timestamp': 'Event timestamp',
        'Execution Timestamp': 'Execution Timestamp',
        'Expiration Date': 'Expiration Date',
        'Notional Amount 1': 'Notional amount-Leg 1',
        'Notional Currency 1': 'Notional currency-Leg 1',
        'Total Notional Quantity 1': 'Total notional quantity-Leg 1',
        'Price 1': 'Price',
        'Price Unit Of Measure 1': 'Price unit of measure',
        'Underlying Asset ID': 'Underlier ID-Leg 1',
        'Underlying Asset ID Type': 'Underlier ID source-Leg 1'
    }

    print(f"Renaming column names of df: {df} \n according to this map: {column_map}")
    
    df.rename(columns=column_map)
    print(f"Rename successful: {df}")


    # # # Drop other columns
    # if trim_source == True:
    # print("Dropping irrelevant columns..")
    # df = df[list(column_map.values())]
    # print(f"Drop successful: {df}")

    # Drop rows that dont have specified ticker listed as an underlying asset
    # df = df[df["Underlier ID-Leg 1"].str.contains(underlier_filter_str, na=False)]
        
    '''
    SEC Changed some names of labels for the 'Action type' field, 
    making them inconsistent across datasets, so we need to assert uniformity
    '''
    
    # df['swonkid'] = datestring.replace('_', '')

    # df = df.loc[:,df.columns.duplicated()].copy()

    df.replace(',','', regex=True, inplace=True)
    # Convert all float columns to integers if they only contain whole numbers
    for col in df.select_dtypes(include='float').columns:
        if (df[col] % 1 == 0).all():  # Check if all values are whole numbers
            df[col] = df[col].astype('Int64')  # Use 'Int64' for integer type with NaN support

    # df = df.replace(np.nan, '', regex=True)
    # Convert only numeric columns to integers
    # df = df.apply(lambda x: pd.to_numeric(x, errors='coerce').fillna(0).astype(int) if pd.api.types.is_numeric_dtype(x) else x)

        # Identify datetime columns
    # Convert numeric columns to integers, ignoring datetime columns
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)

    for col in df.select_dtypes(include='float').columns:
        # Check if all values are whole numbers
        if (df[col] % 1 == 0).all():
            df[col] = df[col].astype('Int64', errors='ignore')

    # Convert boolean columns to strings
    # bool_columns = df.select_dtypes(include=['bool']).columns
    # df[bool_columns] = df[bool_columns].astype(str)

    # Convert object columns to appropriate types
    # object_columns = df.select_dtypes(include=['object']).columns.difference(df.select_dtypes(include=['datetime']).columns)
    # df[object_columns] = df[object_columns].apply(pd.to_numeric, errors='coerce').fillna(0).astype(str)

    # Fill NaN values in non-numeric columns with empty strings
    df = df.fillna('')

    if 'Expiration Date' in df.columns:
        print(df['Expiration Date'])
        # df['Expiration Date'] = df['Expiration Date'].astype(str).str[:8]
        df['Expiration Date'] = pd.to_datetime(df['Expiration Date'], errors='coerce')
        # df['Expiration Date'] = df['Expiration Date'].fillna(pd.Timestamp('1970-01-01'), inplace=True)
    else:
        print("Column 'Expiration_Date' not found.")

    print(df)

    # Option 2: Drop rows with N aT values
    df.dropna(subset=['Expiration Date'], inplace=True)


    # date_fixed = cast_columns(df=df, columns=['Effective Date', 'Expiration Date', 'Execution Timestamp', 'Event timestamp', 'First exercise date'], dtype='datetime64[ns]')
    print('cleaned df', df)
    df = df[list(column_map.values())]
    print("\nFixng action type")
    # Check if 'Action type' column exists
    if 'Action type' in df.columns:
        # Fill missing values
        df['Action type'] = df['Action type'].fillna(False)
        # Replace specific values
        df['Action type'] = df['Action type'].replace({
            'CORRECT': 'CORR',
            'CANCEL': 'TERM',
            'NEW': 'NEWT'
        })
    # Remove duplicate columns by keeping only the first occurrence
    df = df.loc[:, ~df.columns.duplicated()]


    return df


def download_batch(start_date, end_date, table_name, ch_settings):
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

        
        try:
            df = download_and_unzip(url)
        except:
            continue
        print("Data retreived: ", df)
        cleaned = clean_df(df)
        cleaned['Date'] = pd.to_datetime(datestring, format='%Y_%m_%d')

        print("loading df:\n ", cleaned.head(3))
        print(cleaned.dtypes)
        print("using ch settings: ", ch_settings)
        create_table_from_df(df=cleaned, table_name=table_name, settings=ch_settings)
    
        print("loading into clickhouse")
        df_to_clickhouse(df=cleaned, table_name=table_name, settings=ch_settings)
        print("\n\nSuccess!")
 
        
            
def load_csv_to_duckdb(csv, table_name):
    df = pd.read_csv(csv)
    print(df.columns)
    if 'Unique product identifier' not in df.columns:
        df['Unique product identifier'] = None
    
    # Check if the table exists
    table_exists = con.execute(f"""
        SELECT count(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
    """).fetchone()[0] == 1

    
    if table_exists:
        try:
            con.execute(f"""ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS "Unique product identifier" VARCHAR""")
        except Exception as e:
            print(e)
        # Insert data into the existing table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        # Create a new table and insert data
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

    # Iterate through all CSV files in the specified directory



def process_ice_data(swaps_dir, table_name):
    files = glob(f'{swaps_dir}/SECTicker_export_*')

    for file in files:
        # table_name = os.path.splitext(filename)[0]  # Use the filename (without extension) as the table name
        print(f'Loading {file} into table {table_name}')
        load_csv_to_duckdb(file, table_name)





def create_table_from_df(df, table_name, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])
    df.columns = df.columns.str.strip().str.replace(' ', '_')   # Remove spaces from column names
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

    df.columns = df.columns.str.strip().str.replace(' ', '_')   # Remove spaces from column names

    # create_table_from_df(df, table_name=table_name, settings=settings)
    print("\n\nInserting from df: ", df)
    ch_conn.insert_df(table_name, df)
    print("\nSuccess")


def load_df_to_duckdb(df, table_name, db_path):
    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    df.reset_index(drop=True, inplace=True)
    df['Source Entity'] = 'NYSE'
    df['Trade Type'] = 'OTC'
    con = duckdb.connect(database=db_path, read_only=False)
    # Ensure the table exists with the correct schema
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            "Symbol" VARCHAR,
            "Security Name" VARCHAR,
            "Market Category" VARCHAR,
            "Reg SHO Threshold Flag" VARCHAR,
            "Filler" VARCHAR,
            "Date" DATE,
            "Source Entity" VARCHAR,
            "Source URL" VARCHAR,
            "Trade Type", VARCHAR
        )
    """
    con.execute(create_table_query)

    # Insert the data into the table
    columns = ', '.join([f'"{col}"' for col in df.columns])
    insert_query = f"INSERT INTO {table_name} ({columns}) SELECT {columns} FROM df"
    con.execute(insert_query)

    con.close()



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
    Args:
    start_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)
    end_date: String
    '''
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

        # Insert df to db or save to csv

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


# master = filter_merge()
# master=master.drop(columns=['Unnamed: 0'])

# master.to_csv(r"C:\Users\Andym\OneDrive\Documents\SwapsFiltered\filtered.csv") #replace with desired path for successfully filtered and merged report

con = duckdb.connect(database='../data/gme.duckdb', read_only=False)

# Yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # Function requires string input so use strftime to convert

ch_settings = {
    'host': '192.168.8.246',
    'port': 8123,
    'database': 'default',
    'username': 'default',
    'password': ''
}
# print(yesterday)
download_batch('20190723', yesterday, table_name, ch_settings=ch_settings)

# con.execute(f"""
#     COPY {tabe_name} 
#     TO {table_name}.csv 
#     (HEADER, DELIMITER ',')
#     """);


# process_ice_data(swaps_dir, 'ICE_swaps')


# Close the DuckDB connection
con.close()   


