import pandas as pd
import argparse
import asyncio
from spotlight_utils.main import get_token, create_table_from_dict, generate_datestrings, fetch_with_adaptive_concurrency
from config import ice_source_schema as schema_dict



async def main(start_date='20240101', end_date='today', schema_dict=schema_dict, token=None, table_name='Swaps_ICE_source'):
    ''' Grab records from ICE US SDR in parallel for a given range of dates '''
    
    if token is None: # Get token if it wasn't provided
        token = await get_token("https://tradevault.ice.com/tvsec/ticker/webpi/getToken")
        print("Got token ", token)
    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    urls = [f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={datestring[:4]}-{datestring[4:6]}-{datestring[6:8]}' for datestring in datestrings]


    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='_Record_ID')   # Create staging table

    await fetch_with_adaptive_concurrency(
        urls=urls,
        token=token,
        table_name=table_name,
        chunk_size=100000,
        transform_func=transform_df
    )

def transform_df(df: pd.DataFrame, url: str) -> pd.DataFrame:
    ''' Pass this into fetch pipeline to transform dataframes mid-stream '''

    df['_Record_ID'] = df['Dissemination identifier'] + \
        df['Event timestamp'].astype(str).str.replace(r'[-:TZ]', '', regex=True)
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('_-_', '_')
        .str.replace('-', '_')
        .str.replace('/', '_')
    )    
    df = df.astype(str)
    df.replace('nan', None, inplace=True)   # Ensure clickhouse handles null values properly
    df['_Source_URL'] = url

    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Fetch and process CSV data from ICE US SDR.")
    parser.add_argument('--start_date', type=str, default='20240101', help='Start date in YYYYMMDD format')
    parser.add_argument('--end_date', type=str, default='today', help='End date in YYYYMMDD format (or "today")')
    parser.add_argument('--table_name', type=str, default='Swaps_ICE_source', help='Table name for ClickHouse')
    parser.add_argument('--token', type=str, help='Authentication token for API requests')

    args = parser.parse_args()

    asyncio.run(main(start_date=args.start_date, end_date=args.end_date, token=args.token, table_name=args.table_name))