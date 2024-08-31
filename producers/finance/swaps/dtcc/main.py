import pandas as pd
import argparse
import asyncio
from spotlight_utils.main import create_table_from_dict, generate_datestrings, fetch_with_adaptive_concurrency
from config import dtcc_source_schema, dtcc_source_schema2


''' Schema changes on 20240126 -- Use this function with two different schemas depending on dates being pulled. '''


async def main(start_date='20240126', end_date='today', schema_dict=dtcc_source_schema2, token=None, table_name='Swaps_DTCC_source'):
    ''' Grab records from DTCC US SDR in parallel for a given range of dates '''
        
    ''' Schema was changed on 20240126 -- make sure to select batches non overlapping with this date ''' 
    schema_dict = dtcc_source_schema2 if int(start_date) >= 20240126 else dtcc_source_schema

    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    
    urls = [gen_dtcc_url('SEC', 'CUMULATIVE', 'EQUITIES', '_'.join([datestring[:4], datestring[4:6], datestring[6:8]])) for datestring in datestrings] # This function can be used for pulling from cftc and other asset classes

    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='_Record_ID')   # Create staging table

    print("Requesting swap records from DTCC for dates: ", datestrings)
    await fetch_with_adaptive_concurrency(
        urls=urls,
        table_name=table_name,
        chunk_size=100000,
        transform_func=transform_df
    )



def gen_dtcc_url(jurisdiction, report_type, asset_class, datestring):
    dtcc_url = 'https://pddata.dtcc.com/ppd/api/report'
    return f'{dtcc_url}/{report_type.lower()}/{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestring}.zip'



def transform_df(df: pd.DataFrame, url: str) -> pd.DataFrame:
    ''' Pass this into fetch pipeline to transform dataframes mid-stream '''

    df['_Record_ID'] = df['Dissemination Identifier'].astype(str) + \
        df['Event timestamp'].astype(str).str.replace(r'[-:TZ]', '', regex=True)
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('_-_','_')
        .str.replace('-','_')
        .str.replace('/','_')  # Remove spaces from column names
    )
    df = df.astype(str)
    df.replace('nan', None, inplace=True)   # Ensure clickhouse handles null values properly
    df['_Source_URL'] = url
    
    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Fetch and process CSV data from DTCC US SDR.")
    parser.add_argument('--start_date', type=str, default='20240101', help='Start date in YYYYMMDD format')
    parser.add_argument('--end_date', type=str, default='today', help='End date in YYYYMMDD format (or "today")')
    parser.add_argument('--table_name', type=str, default='Swaps_DTCC_source', help='Table name for ClickHouse')
    args = parser.parse_args()

    asyncio.run(main(start_date=args.start_date, end_date=args.end_date, table_name=args.table_name))