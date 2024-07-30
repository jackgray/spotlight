import json
import duckdb
from pyspark.sql import SparkSession as session
from pyspark.sql.functions import col, to_date, upper
# from duckdb.experimental.spark.sql import SparkSession as session
# from duckdb.experimental.spark.sql.functions import lit, col, to_date
import polars as pl
from datetime import datetime

from api import get_all_sheets_data
import os



db_name = 'gme'
db_file = f'../{db_name}.duckdb'
sourcedata_path = '../sourcedata'
rawdata_path = '../rawdata'

# try:
#     # Initialize Spark session
#     spark = session.builder \
#         .appName("JSON to DuckDB") \
#         .getOrCreate()
# except:
#     useSpark = False

useSpark = False


def parse_date(date_str):
    '''
    Parse a date string using multiple formats and return ISO format.
    '''
    date_formats = [
        "%m/%d/%Y",    # Example: 12/31/2020
        "%Y-%m-%d",    # Example: 2020-12-31
        "%d-%b-%Y",    # Example: 31-Dec-2020
        "%d/%m/%Y",    # Example: 31/12/2020
        "%d-%b-%y",    # Example: 31-Dec-21
        "%d-%m-%Y",    # Example: 31-12-2020
        "%b %d, %Y",   # Example: Dec 31, 2020
        "%b %d, %y"    # Example: Dec 31, 20
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date().isoformat()
        except ValueError:
            continue
    return None  # Return None if no format matches

def parse_dates(df, date_columns):
    '''
    Parse dates with multiple formats and convert to ISO format.
    '''
    for column in date_columns:
        # Apply the parse_date function to each entry in the date column
        try:
            df = df.with_columns(
                pl.col(column).map_elements(parse_date, return_dtype=pl.Utf8).alias(column)
            )
        except:
            pass   
    return df

# Function to load data from JSON files into DuckDB and export to CSV
def load(table_name, db_file):

    '''
    Reads raw download of csv file and loads into duckdb database
    '''

    os.makedirs('rawdata', exist_ok=True)  # Ensure rawdata directory exists

    # open DB
    con = duckdb.connect(database=db_file, read_only=False)

    in_file = f'{sourcedata_path}/{table_name}.csv'
    out_file = f'{rawdata_path}/{table_name}.csv'

    # read CSV
    if useSpark is not False:
        try:
            df = spark.read.csv(in_file)
            df = df.withColumn("Date", to_date(col("Date"), "yyyy-MM-dd"))
        except:
            df = pl.read_csv(in_file, try_parse_dates=True)
    else:
        df = pl.read_csv(
            in_file, 
            schema_overrides={
                'XRTvol': pl.Float64,
            },
            infer_schema_length=10000,
            try_parse_dates=True,
            ignore_errors=True
        )
        
        # Remove commas from numeric columns
        problem_cols = ['XRTvol']
        numeric_columns = [col for col in df.columns if col in problem_cols]  # Add all numeric columns that might have commas
        df = df.with_columns([
            pl.col(col).str.replace_all(",", "").cast(pl.Float64, strict=False)
            for col in numeric_columns  # Assuming `columns` is a list of column names you want to process
        ])

        df = parse_dates(df, ['Date'])

    con.execute(f"""
        CREATE OR REPLACE TABLE {table_name}
        AS SELECT *
        FROM df
    """)

    # Export the DuckDB table to CSV
    print(f"Saving table: {table_name} to file: {out_file}")
    try:
        con.execute(f"""
            COPY {table_name} 
            TO '{out_file}' (HEADER, DELIMITER ',', DATEFORMAT '%Y-%m-%d', TIMESTAMPFORMAT '%A, %-d %B %Y - %I:%M:%S %p');
        """)
    except Exception as e:
        print(e)

    con.close()




def download_sourcedata():

    '''
    Calls google sheets api wrapper and saves results to json files
    '''

    try:
        data = get_all_sheets_data()
    except Exception as e:
        print(f"Could not download data from internet \n {e}")


    

def populate(sourcedata_path):

    '''
    Iterates through files in sourcedata and loads them into duckdb tables and exports them as csv files to rawdata
    '''

    # Ensure the directory exists
    if not os.path.exists(sourcedata_path):
        print(f"Directory {sourcedata_path} does not exist.")
        return json_data

    # List all files in the directory
    filelist = os.listdir(sourcedata_path)

    # Gather all JSON files in source dir
    files = [f for f in filelist if f.endswith('.csv')]

    # Save data to JSON files and collect table names
    for file in files:
        table_name = file.split('/')[-1].split('.')[0]
        print(f'Saving data for table: {table_name}')
    
        # Load data from JSON files into DuckDB and export to CSV
        load(table_name, db_file)




if __name__ == "__main__":
    # download_sourcedata()
    populate(sourcedata_path)
