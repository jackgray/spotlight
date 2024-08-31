import pandas as pd
import argparse
import asyncio
from airflow import DAG
from airflow.operators.python import PythonOperator

from spotlight_utils.main import get_token, create_table_from_dict, generate_datestrings, fetch_with_adaptive_concurrency
from config import ice_source_schema as schema_dict





# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 31),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'dagrun_timeout': timedelta(hours=2),
    'pool': 'my_pool',
    'priority_weight': 10,
    'execution_timeout': timedelta(hours=1),
    'queue': 'default',
    'on_failure_callback': failure_callback,
    'on_retry_callback': retry_callback,
    'on_success_callback': success_callback,
}






# Define the DAG
dag = DAG(
    'fetch_swap_equities_from_ice',
    default_args=default_args,
    description='DAG to fetch CSV data from multiple URLs using asyncio',
    schedule_interval=timedelta(days=1),  # Set the desired interval (daily, weekly, etc.)
)





run_task = PythonOperator(
    task_id=f'fetch_ice_swaps_equity_{start_date}-{end_date}',
    python_callable=fetch_data,
    op_kwargs={
        'start_date': 'yesterday',
        'end_date': 'today',
        'schema_dict'=schema_dict,
        'table_name': 'Swaps_ICE_source_af',  # Replace with your actual table name
    },
    dag=dag,
)






async def main(start_date='yesterday', end_date='today', schema_dict=schema_dict, token=None, table_name='Swaps_ICE_source', spark = False, **kwargs):
    ''' Grab records from ICE US SDR in parallel for a given range of dates '''
    
    if token is None: # Get token if it wasn't provided
        token = await get_token("https://tradevault.ice.com/tvsec/ticker/webpi/getToken")
        print("Got token ", token)
    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    urls = [f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={datestring[:4]}-{datestring[4:6]}-{datestring[6:8]}' for datestring in datestrings]


    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='_Record_ID')   # Create staging table

    fetch_data():
        if spark:
            conf = SparkConf().setAppName("FetchAndLoadZippedCSV").setMaster("local[*]")
            sc = SparkContext(conf=conf)
            spark = SparkSession(sc)

            # Convert the list of URLs into an RDD
            urls_rdd = sc.parallelize(urls)

            results = urls_rdd.map(lambda url: fetch_and_load_csv(
                url=url,    # Apply the fetch_and_load_zipped_csv function to each URL
                token=token,
                table_name=table_name, 
                chunk_size=100000, 
                ch_settings=None, 
                transform_func=transform_df  # Or pass your custom transformation function
            )).collect()

            # Sum up the total rows processed
            total_rows = sum(results)
            print(f"Total rows processed across all URLs: {total_rows}")
        else:
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

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    if args.spark == True:
        run (help)

    else:
        run_task
        # asyncio.run(main(start_date=args.start_date, end_date=args.end_date, token=args.token, table_name=args.table_name))