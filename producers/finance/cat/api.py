from datetime import datetime, timedelta
import requests
import pdfplumber
import pandas as pd
import pandahouse as ph
import duckdb
from io import BytesIO
from typing import Optional, Required, List, Union
from clickhouse_connect import get_client as ch
import re


def fetch_pdf_to_list(datestring):
    """Fetch PDF from URL and extract text from the last 8 pages as a list of strings."""
    monthstring = datetime.strptime(datestring, '%Y%m%d').strftime('%Y-%m')
    datestring_fmt = datetime.strptime(datestring, '%Y%m%d').strftime('%m.%d.%y')

    url = f'https://www.catnmsplan.com/sites/default/files/{monthstring}/{datestring_fmt}-Monthly-CAT-Update.pdf'

    response = requests.get(url)
    pdf_bytes = BytesIO(response.content)

    try:
        text = []
        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages[-8:]:
                table = page.extract_table()
                if table != None:
                    text.append(page.extract_table())
        # print(len(text))
        return text, url
    except Exception as e:
        return None


def clean_to_df(data, params):
    columns = list(params['schema'].keys())
    print("Padding columns: ", columns)
    
    padded = [row[:len(columns)] + [None] * (len(columns) - len(row[:len(columns)])) for row in data]
    df2 = pd.DataFrame(padded, columns=columns)
    
    print("Cleaning df: ", df2.head(3))
    
    # Remove rows with non-date values in 'Date' column
    df2 = df2[~df2['Date'].str.contains('Trade|Date', na=False)].copy()
    
    try:
        df2['Date'] = pd.to_datetime(df2['Date'], format=params['date format'])
    except ValueError as e:
        print(f"Error parsing date: {e}")
    
    df2 = df2.replace(' ', '', regex=True).replace('%', '', regex=True).replace(',', '', regex=True).reset_index(drop=True)
    
    for column, dtype in params['schema'].items():
        if column in df2.columns:
            try:
                df2[column] = df2[column].astype(dtype)
            except Exception as e:
                print(f'Problem setting type for column {column}')
                print(e)
    
    return df2



def df_to_clickhouse(df, table_name, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])
    ch_conn.insert_df(table_name, df)


def cat_by_date(datestring, ch_settings, db_path='default_data.duckdb'):

    """Process the PDF data and load it into DuckDB."""
    try:
        data, url = fetch_pdf_to_list(datestring)
    except:
        return None

    dynamic_slices = generate_slices(len(data))

    params = { 
        'rolling': {
            'schema': {
                'Date': 'datetime64[ns]',
                'Late': 'float',
                'Rejection_Initial': 'float',
                'Rejection_Adjusted': 'float',
                'Intrafirm_Initial': 'float',
                'Intrafirm_Adjusted': 'float',
                'Interfirm_Sent_Initial': 'float',
                'Interfirm_Sent_Adjusted': 'float',
                'Interfirm_Received_Initial': 'float',
                'Interfirm_Received_Adjusted': 'float',
                'Exchange_Initial': 'float',
                'Exchange_Adjusted': 'float',
                'Trade_Initial': 'float',
                'Trade_Adjusted': 'float',
                'Overall_Error_Rate_Initial': 'float',
                'Overall_Error_Rate_Adjusted': 'float',
                'Trade_Type': 'str',
                'Report_Date': 'datetime64[ns]',
                'Source_URL': 'str',
                'ID': 'str',
            },
            'date format': '%m/%d/%Y',
            'pages': dynamic_slices['rolling']
        },
        'trade stats': {
            'schema': {
                'Date': 'datetime64[ns]',
                'Processed': 'int',
                'Accepted': 'int',
                'Late': 'int',
                'Overall_Errors_Count': 'int',
                'Trade_Type': 'str',
                'Report_Date': 'datetime64[ns]',
                'Source_URL': 'str',
                'ID': 'str'
            },
            'date format': '%Y-%m-%d',
            'pages': dynamic_slices['trade stats']
        }
    }

    print("\n\n\n\n*******\nFetched CAT data from ", url)
    # print(text)
    for report in params:
        combined_df = pd.DataFrame()  # Initialize an empty DataFrame for combining
        
        for trade_type in params[report]['pages']:
            print(f"\nProcessing: {report}-{trade_type}")
            # data = [item for item in text if item is not None]
            # Pull for specific trade type (Options or Equities)
            rawdata = data[params[report]['pages'][trade_type]]
            # Get data into formatted list
            try:
                combined = [row for sublist in rawdata for row in sublist[1:]]
            except:
                combined = rawdata
            # Convert to df
            print(f"Converting {report} report to df...")
            df = clean_to_df(data=combined, params=params[report])
            # Generate unique ID for each entry
            df['ID'] = 'cat' + report.lower()[:3] + df['Date'].dt.strftime('%Y%m%d').replace('-', '') + trade_type[:2]
            df['Report_Date'] = datetime.strptime(datestring, '%Y%m%d').strftime('%Y-%m-%d')
            df['Source_URL'] = url
            # df['Data Provider'] = 'FINRA'     # Currently this is the only provider so it's implied
            df['Trade_Type'] = trade_type.capitalize()  # Add the trade type column

            print(f'\nCombiniing dfs: {df.head} & {combined_df}') 
            # Combine with the previous DataFrame
            combined_df = pd.concat([combined_df, df])

        # Determine the table name based on the report type
        rptname=report.capitalize().replace(' ', '_')
        table_name = f'CAT_{rptname}'
        # Load the combined DataFrame into DuckDB
        # load_to_duckdb(combined_df, table_name, params=params[report], con=con)
        
        print(f"Trying to load into clickhouse...")
        try:    
            create_table_from_df(df=combined_df, table_name=table_name, settings=ch_settings)
            df_to_clickhouse(df=combined_df, table_name=table_name, settings=ch_settings)
            print("...Success")
        except Exception as e:
            print(e)

def cat_by_range(start_date, end_date, ch_settings, db_path='../../../data/stonk.duckdb'):
    print(f"Pulling data for date range: {start_date}-{end_date}")
    for datestring in generate_date_strings(start_date=start_date, end_date=end_date):
        res = cat_by_date(datestring, ch_settings=ch_settings, db_path=db_path)
        if res == None:
            continue



###########
#  UTILS
###########

def generate_slices(total_pages):
    """
    Generate dynamic slices for 'pages' based on total number of pages and page size.

    Args:
    - total_pages (int): Total number of pages available.
    - page_size (int): Size of each page group.

    Returns:
    - dict: A dictionary with dynamic slices for 'equities' and 'options'.
    """
    idx = total_pages // 4

    # Generate slices based on the number of groups
    slices = {
        'rolling': {
            'equities': slice(0, min(idx, total_pages)),
            'options': slice(idx, min(idx * 2, total_pages))
        },
        'trade stats': {
            'equities': slice(2 * idx, 3 * idx),
            'options': slice(3 * idx, 4 * idx),
        }
    }
    return slices

def create_table_from_df(df, table_name, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

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
        ORDER BY tuple()
    """
    ch_conn.command(create_table_query)

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


def duckdb_to_clickhouse(db_path='./stonk.duckdb', ch_host='localhost', ch_port=8123, ch_db='default', ch_user='default'):
    """
    Load all tables in DuckDB database to ClickHouse in a single batch.
    """
    import duckdb
    from clickhouse_connect import get_client as ch
    import pandas as pd

    # Connect to DuckDB
    con = duckdb.connect(db_path)
    
    # Retrieve all table names from the DuckDB database
    table_names = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()
    
    # Connect to ClickHouse
    client = ch(host=ch_host, port=ch_port, username=ch_user, database=ch_db)
    
    # Define a function to map ClickHouse types to Pandas dtypes
    def clickhouse_to_pandas_type(ch_type):
        if ch_type == 'DATE':
            return 'datetime64[ns]'
        elif ch_type == 'INTEGER':
            return 'Int64'  # Int64 for nullable integers in Pandas
        elif ch_type == 'FLOAT64':
            return 'float64'
        elif ch_type == 'VARCHAR':
            return 'str'
        elif ch_type == 'BOOLEAN':
            return 'bool'
        else:
            return 'str'  # Default to str for unknown types

    # Iterate over each table and load it into ClickHouse
    for (table_name,) in table_names:
        # Load table into a Pandas DataFrame
        df = con.execute(f"SELECT * FROM {table_name}").df()
        
        # Fetch ClickHouse table schema
        clickhouse_columns = client.query(f'DESCRIBE TABLE {table_name}').result_rows
        clickhouse_column_types = {row[0]: row[1] for row in clickhouse_columns}

        # Dynamically convert DataFrame columns to match ClickHouse schema
        for col, ch_type in clickhouse_column_types.items():
            if col in df.columns:
                pandas_type = clickhouse_to_pandas_type(ch_type)
                df[col] = df[col].astype(pandas_type, errors='ignore')

        # Replace spaces with underscores in column names
        df.columns = df.columns.str.replace(' ', '_')
        
        # Convert DataFrame to list of tuples
        data_tuples = list(df.itertuples(index=False, name=None))
        
        # Print row data types for debugging
        for row in data_tuples:
            print("Row data types:", [type(item) for item in row])
        
        # Insert the DataFrame into ClickHouse
        try:
            client.insert(table_name, data_tuples, column_names=list(df.columns))
        except Exception as e:
            print(f"Error inserting data into table {table_name}: {e}")
        
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