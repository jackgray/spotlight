from datetime import datetime, timedelta
import requests
import pdfplumber
import pandas as pd
import duckdb
from io import BytesIO
from typing import Optional, Required, List, Union


def fetch_pdf_to_list(datestring):
    """Fetch PDF from URL and extract text from the last 8 pages as a list of strings."""
    monthstring = datetime.strptime(datestring, '%Y%m%d').strftime('%Y-%m')
    datestring_fmt = datetime.strptime(datestring, '%Y%m%d').strftime('%m.%d.%y')

    url = f'https://www.catnmsplan.com/sites/default/files/{monthstring}/{datestring_fmt}-Monthly-CAT-Update.pdf'

    response = requests.get(url)
    pdf_bytes = BytesIO(response.content)

    text = []
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages[-8:]:
            text.append(page.extract_text().split('\n'))
    return text, url


def clean_list(raw_data, params):
    """Clean raw data by slicing and flattening it into a single list."""
    all_data = [raw_data[i][params['slice']] for i in range(len(raw_data))]
    combined_list = [item for sublist in all_data for item in sublist]
    return combined_list


def clean_to_df(data, params):
    """Convert cleaned list data into a DataFrame and format the Date column."""
    df = pd.DataFrame([row.split() for row in data], columns=params['columns'])
    df['Date'] = pd.to_datetime(df['Date'], format=params['date format']).dt.strftime('%Y-%m-%d')
    df = df.replace('%', '', regex=True).reset_index(drop=True)
    return df


def load_to_duckdb(df, table_name, params, con):
    """Load the DataFrame into a DuckDB table named by the report and trade_type."""

    print(f"Inserting cleaned dataframe: {df.head(3)}")

    # Infer schema from dataframe with helper function
    schema = get_duckdb_schema_from_df(df)
    # Ensure the table exists with the correct schema
    try:
        con.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} ( {schema} ) """)
    except Exception as e: 
        print(f"\n\n******ERROR******\nCould not make table {table_name} \n {e}\n\n\n")
        return None

    # Insert the data into the table
    try: 
        con.execute(f"""
            INSERT INTO {table_name} BY NAME
            SELECT * FROM df
        """)
        print("Inserted df into duckdb table")
    except Exception as e: 
        print(f'\n\n**********ERROR*******\nDB LOAD FAILED {e}\n\n')

    return df

def cat_by_date(datestring, params, db_path='default_data.duckdb'):
    """Process the PDF data and load it into DuckDB."""
    text, url = fetch_pdf_to_list(datestring)
    con = duckdb.connect(db_path)
    print("\n\n\n\n*******\nFetched CAT data from ", url)
    # print(text)
    for report in params:
        # print(params[report]['pages'])
        combined_df = pd.DataFrame()  # Initialize an empty DataFrame for combining
        for trade_type in params[report]['pages']:
            print(f"\nProcessing: {report}-{trade_type}")

            # Pull for specific trade type (Options or Equities)
            rawdata = text[params[report]['pages'][trade_type]]
            # Get data into formatted list
            cleaned = clean_list(rawdata, params=params[report])

            # Convert to df
            df = clean_to_df(data=cleaned, params=params[report])
            # Generate unique ID for each entry
            df['ID'] = df['Date'].str.replace('-', '') + trade_type[:2]
            df['Source URL'] = url
            # df['Data Provider'] = 'FINRA'     # Currently this is the only provider so it's implied
            df['Trade Type'] = trade_type.capitalize()  # Add the trade type column
            # Combine with the previous DataFrame
            combined_df = pd.concat([combined_df, df])

        # Determine the table name based on the report type
        rptname=report.capitalize().replace(' ', '_')
        table_name = f'CAT_{rptname}'
        # Load the combined DataFrame into DuckDB
        load_to_duckdb(combined_df, table_name, params=params[report], con=con)
        
    con.close()


def cat_by_range(start_date, end_date, db_path='../../../data/stonk.duckdb'):
    
    params = { 
        'rolling': {
            'columns': [
                'Date', 'Late', 'Rejection Initial', 'Rejection Adjusted', 
                'Intrafirm Initial', 'Intrafirm Adjusted', 'Interfirm Sent Initial', 
                'Interfirm Sent Adjusted', 'Interfirm Received Initial', 
                'Interfirm Received Adjusted', 'Exchange Initial', 'Exchange Adjusted', 
                'Trade Initial', 'Trade Adjusted', 'Overall Error Rate Initial', 
                'Overall Error Rate Adjusted' #, 'ID', 'Trade Type', 'Source URL'
            ],
            'date format': '%m/%d/%Y',
            'slice': slice(5, -1),
            'pages': {
                'equities': slice(0, 2),
                'options': slice(2, 4)
            } 
        },
        'trade stats': {
            'columns': ['Date', 'Processed', 'Accepted', 'Late', 'Overall Errors Count'],
            'date format': '%Y-%m-%d',
            'slice': slice(3, -1),
            'pages': {
                'equities': slice(4, 6),
                'options': slice(6, 8)
            }
        }
    }

    
    
    for datestring in generate_date_strings(start_date=start_date, end_date=end_date):
        try:
            cat_by_date(datestring, params=params, db_path=db_path)
        except: pass



###########
#  UTILS
###########

def duckdb_to_clickhouse(db_path='./stonk.duckdb', ch_host='localhost', ch_port=8123, ch_db='default', ch_user='default'):
    """
    Load all tables in DuckDB database to ClickHouse in a single batch.
    """
    import duckdb
    from clickhouse_connect import get_client as ch
    import pandas as pd
    import numpy as np

    # Connect to DuckDB
    con = duckdb.connect(db_path)
    
    # Retrieve all table names from the DuckDB database
    table_names = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
    
    # Connect to ClickHouse
    client = ch(host=ch_host, port=ch_port, username=ch_user, database=ch_db)
    
    # Iterate over each table and load it into ClickHouse
    for (table_name,) in table_names:
        # Load table into a Pandas DataFrame
        df = con.execute(f"SELECT * FROM {table_name}").df()
        
        # Replace spaces with underscores in column names
        df.columns = df.columns.str.replace(' ', '_')
        print("\nDataFrame Columns: ", df.columns)
        
        # Handle `None` values in DataFrame by converting them to empty strings
        df = df.fillna('')
        
        # Infer the schema for the ClickHouse table
        dtype_mapping = {
            'int64': 'Int64',
            'float64': 'Float64',
            'object': 'String',
            'bool': 'UInt8',
            'datetime64[ns]': 'DateTime',
            'uint64': 'UInt64'
        }
        
        # Handle datetime conversion
        def map_dtype(dtype):
            if 'datetime' in dtype:
                return 'DateTime'
            return dtype_mapping.get(dtype, 'String')
        
        columns = ', '.join([f"`{col}` {map_dtype(str(dtype))}" 
                             for col, dtype in zip(df.columns, df.dtypes)])
        print("\nCreate Table Query: ", columns)
        
        # Drop the existing table if it exists
        client.command(f"DROP TABLE IF EXISTS {table_name}")
        
        # Create the table in ClickHouse
        create_table_query = f"""
        CREATE TABLE {table_name} ({columns}) 
        ENGINE = MergeTree() 
        ORDER BY tuple()
        """
        client.command(create_table_query)
        
        # Fetch ClickHouse table schema
        clickhouse_columns = client.query(f'DESCRIBE TABLE {table_name}').result_rows
        clickhouse_column_names = [row[0] for row in clickhouse_columns]
        print("ClickHouse table columns:", clickhouse_column_names)
        
        # Ensure all columns in the DataFrame exist in ClickHouse table
        missing_columns = set(df.columns) - set(clickhouse_column_names)
        if missing_columns:
            raise ValueError(f"Columns {missing_columns} are missing in the ClickHouse table {table_name}")
        
        # Insert the DataFrame into ClickHouse
        # Convert DataFrame to list of tuples
        data_tuples = [tuple(x) for x in df.to_numpy()]
        client.insert(table_name, data_tuples, column_names=list(df.columns))
        
        print(f"Loaded table {table_name} into ClickHouse.")
    
    # Close DuckDB connection
    con.close()
    
    print("All tables loaded successfully.")






def get_duckdb_schema_from_df(df):
    """
    Maps the provided columns to DuckDB-compatible data types.
    """
    schema_map = {
        'ID': 'VARCHAR',
        'Date': 'DATE',
        'Late': 'FLOAT',
        'Rejection Initial': 'FLOAT',
        'Rejection Adjusted': 'FLOAT',
        'Intrafirm Initial': 'FLOAT',
        'Intrafirm Adjusted': 'FLOAT',
        'Interfirm Sent Initial': 'FLOAT',
        'Interfirm Sent Adjusted': 'FLOAT',
        'Interfirm Received Initial': 'FLOAT',
        'Interfirm Received Adjusted': 'FLOAT',
        'Exchange Initial': 'FLOAT',
        'Exchange Adjusted': 'FLOAT',
        'Trade Initial': 'FLOAT',
        'Trade Adjusted': 'FLOAT',
        'Overall Error Rate Initial': 'FLOAT',
        'Overall Error Rate Adjusted': 'FLOAT',
        'Processed': 'BIGINT',
        'Accepted': 'BIGINT',
        'Overall Errors Count': 'BIGINT',
        'Trade Type': 'VARCHAR',
        'Source URL': 'VARCHAR'
    }

    schema = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        duckdb_type = schema_map.get(dtype, 'VARCHAR')  # Default to VARCHAR if dtype is not mapped
        if col == 'ID':
            duckdb_type += ' PRIMARY KEY'
        schema.append(f'"{col}" {duckdb_type}')

    # Map the columns to their DuckDB data types
    return ", ".join(schema)


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