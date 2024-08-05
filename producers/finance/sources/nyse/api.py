'''
Retrieves data from NYSE download links

'''

import requests
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
import duckdb
from producers.finance.sources.utils.main import regsho_by_range

def gen_nyse_regsho_url(datestring, market='NYSE'):
    '''
    Generates URL string from supplied date

    datestring must be in the format expected by the endpoint -- supplied by:
    for datestring in generate_date_strings(start_date, end_date): 
        url = gen_nasdaq_regsho_url(datestring)

    Used in fetch by date functions to request the proper URL based on date format input parameters
    '''

    return f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={datestring}&market={market}'




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
