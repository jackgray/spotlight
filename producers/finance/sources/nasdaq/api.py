import requests
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
import duckdb
from producers.finance.sources.utils.main import generate_date_strings, regsho_by_date

def gen_nasdaq_regsho_url(datestring):
    '''
    Generates URL string from supplied date

    datestring must be in the format expected by the endpoint -- supplied by:
    for datestring in generate_date_strings(start_date, end_date): 
        url = gen_nasdaq_regsho_url(datestring)

    Used in fetch by date functions to request the proper URL based on date format input parameters
    '''

    return f'http://www.nasdaqtrader.com/dynamic/symdir/regsho/nasdaqth{datestring}.txt'




def load_df_to_duckdb(df, table_name, db_path):
    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    df.reset_index(drop=True, inplace=True)
    df['Source Entity'] = 'Nasdaq'
    df['Trade Type'] = 'Non-OTC'

    con = duckdb.connect(database=db_path, read_only=False)
    # Check if the table exists
    table_exists = con.execute(f"""
        SELECT count(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
    """).fetchone()[0] == 1
    
    if table_exists:
        # Insert data into the existing table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        # Create a new table and insert data
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")


def regsho_by_range(start_date, end_date, urlgen_func, table_name, db_path, from_date_format, to_date_format):
    '''
    Downloads NASDAQ or NYSE RegSHO data files for a range of dates

    Only difference is the URL and date formatting. Table Schema is the same

    Depends on: generate_date_strings(), download_and_unzip()

    Args:
    start_date: String %Y%m%d (e.g. 20240125 = jan 25 2024)
    end_date: String

    Returns: df of values that failed to load into DuckDB

    '''

    # Allow 'yesterday' to be supplied as an input for start or end date
    # If start date is set to 'yesterday' a list of one day (yesterdays date) should be returned
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # Function requires string input so use strftime to convert
    start_date = yesterday if start_date == 'yesterday' else start_date
    end_date = yesterday if end_date == 'yesterday' else end_date

    # Gather properly formated list of datestrings (e.g. "YYYY_MM_dd"to feed into download url string 
    datestrings = generate_date_strings(start_date, end_date, from_date_format, to_date_format)
    print(f"Pulling data for the following dates: {list(datestrings)}")
    dfs=[]
    for datestring in datestrings:
        # Download file
        try: 
            print(f"Downloading data for date: {datestring}")
            df = regsho_by_date(datestring, to_date_format, urlgen_func)
            print(f"Pulled data for {datestring}: {df}")
            try:
                print("Loading to DuckDB...")
                load_df_to_duckdb(df, table_name, db_path)
            except Exception as e:
                print(e)
                print("Appending to dataframe to be returned...")
                dfs.append(df)

        except Exception as e:
            # print('\n\n',e)
            print(f"Could not grab data for date: {datestring} -- Probably tried to download a weekend or holiday date\n\n")

    # Concatenate all DataFrames into a single DataFrame
    final_df = pd.concat(dfs, ignore_index=True)

    return final_df
