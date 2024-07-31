import requests
from zipfile import ZipFile
import os
from os import listdir, path, remove, makedirs, getenv
import duckdb
import pandas as pd
import polars as pl
from datetime import datetime, timedelta
from glob import glob

local_run = True

# table_name = 'sec_swaps_raw'
table_name = 'gme_swaps_raw'


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
    return f'{dtcc_url}/{report_type.lower()}{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestring}.zip'


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


def clean_df(df, underlier_filter_st):
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

    # # Drop other columns
    if trim_source = True:
        print("Dropping irrelevant columns..")
        df = df[list(column_map.values())]
        print(f"Drop successful: {df}")

    # Drop rows that dont have specified ticker listed as an underlying asset
    df = df[df["Underlier ID-Leg 1"].str.contains(underlier_filter_str, na=False)]
        
    '''
    SEC Changed some names of labels for the 'Action type' field, 
    making them inconsistent across datasets, so we need to assert uniformity
    '''

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

    # df['swonkid'] = datestring.replace('_', '')

    df = df.loc[:,~df.columns.duplicated()].copy()

    df.replace(',','', regex=True, inplace=True)
    # c = df.select_dtypes(object).columns
    # df[c] = df[c].apply(pd.to_numeric,errors='coerce')

    return df


def download_batch(start_date, end_date, table_name):
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

            df = clean_df(df, column_map)
       
            # Make sure table exists before trying to append it
            try:
                con.execute(f"""
                    CREATE TABLE {table_name}
                    AS SELECT * from df
                """)
            except:
                print(f"Inserting data into table {table_name}:\n{df}")
                con.execute(f"""
                    INSERT INTO {table_name} BY NAME
                    SELECT * FROM df
                """)
        except:
            continue
        
            
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


# master = filter_merge()
# master=master.drop(columns=['Unnamed: 0'])

# master.to_csv(r"C:\Users\Andym\OneDrive\Documents\SwapsFiltered\filtered.csv") #replace with desired path for successfully filtered and merged report

con = duckdb.connect(database='../data/gme.duckdb', read_only=False)

# Yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # Function requires string input so use strftime to convert

# print(yesterday)
def dowload_all():
    for 
    download_batch('20230723', yesterday, table_name)

# con.execute(f"""
#     COPY {tabe_name} 
#     TO {table_name}.csv 
#     (HEADER, DELIMITER ',')
#     """);


# process_ice_data(swaps_dir, 'ICE_swaps')


# Close the DuckDB connection
con.close()   