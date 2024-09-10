import pandas as pd
import argparse
import asyncio

from spotlight_utils.main import get_token, create_table_from_dict, generate_datestrings, fetch_with_adaptive_concurrency
from config import ice_source_schema as schema_dict

''' 
Usage:

python3.11 main.py. --start_date '20200101' --end_date 'today' --table_name 'Swaps_ICE_source_sept1'

'''



async def main(start_date='yesterday', end_date='today', schema_dict=schema_dict, token=None, table_name='Swaps_ICE_source', spark = False, **kwargs):
    ''' Grab records from ICE US SDR in parallel for a given range of dates '''
    
    if token is None: # Get token if it wasn't provided
        token = await get_token("https://tradevault.ice.com/tvsec/ticker/webpi/getToken")
    
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




def run_spark(start_date, end_date, schema_dict, token, table_name):
    ''' Run Spark processing '''
    
    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    urls = [f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={datestring[:4]}-{datestring[4:6]}-{datestring[6:8]}' for datestring in datestrings]

    conf = SparkConf().setAppName("FetchAndLoadZippedCSV").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    # Convert the list of URLs into an RDD
    urls_rdd = sc.parallelize(urls)

    results = urls_rdd.map(lambda url: fetch_and_load_csv(
        url=url,  # Apply the fetch_and_load_zipped_csv function to each URL
        token=token,
        table_name=table_name, 
        chunk_size=100000, 
        ch_settings=None, 
        transform_func=transform_df  # Or pass your custom transformation function
    )).collect()

    # Sum up the total rows processed
    total_rows = sum(results)
    print(f"Total rows processed across all URLs: {total_rows}")





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



def retry_callback():
    print("retry callback placeholder")

def success_callback():
    print("success callback placeholder")



def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and process CSV data from ICE US SDR.")
    parser.add_argument('--start_date', type=str, default='20240101', help='Start date in YYYYMMDD format')
    parser.add_argument('--end_date', type=str, default='today', help='End date in YYYYMMDD format (or "today")')
    parser.add_argument('--table_name', type=str, default='Swaps_ICE_source', help='Table name for ClickHouse')
    parser.add_argument('--token', type=str, help='Authentication token for API requests')
    parser.add_argument('--spark', type=bool, default=False, help='Whether to run this pipeline using Spark and rdds')

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()

    asyncio.run(main(start_date=args.start_date, end_date=args.end_date, token=args.token, table_name=args.table_name))

