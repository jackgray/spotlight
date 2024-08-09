from datetime import datetime, timedelta
import requests
import pdfplumber
import pandas as pd
import duckdb
from io import BytesIO
from typing import Optional, Required, List, Union

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


# def load_to_duckdb(df, table_name, connection):
#     """Load the DataFrame into a DuckDB table named by the report and trade_type."""
#     print("Generating table name: ", table_name)
#     connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
#     print(f"Loaded data into table: {table_name}")

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


