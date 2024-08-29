
from spotlight_utils.main import get_token, fetch_csv, create_table_from_dict, df_to_clickhouse
from config import ice_source_schema as schema_dict
from config import ch_settings


token = get_token("https://tradevault.ice.com/tvsec/ticker/webpi/getToken") # This function is mostly just a reference -- make sure to run it once instead of for every date (when looping over a range)

async def main(datestring='20240101', schema_dict=schema_dict, token=None, table_name='Swaps_ICE_source', ch_settings=ch_settings):
    ''' Grab record from ICE US SDR for a given date '''
    
    url_datestring = '-'.join([datestring[:4], datestring[4:6], datestring[6:8]])   # Convert date into format url uses
    url = f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={url_datestring}'

    loop = asyncio.get_event_loop()
    csv_results = loop.run_until_complete(fetch_all_csv(urls, token=token))

    logging.info(f"Retrieving {url}")

    df = await fetch_csv(url=url, token=token)

    df['_RecordID'] = df['Dissemination identifier'] + 
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
    df['_Report_Date'] = url_datestring          
    df['_Source_URL'] = url

    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='_RecordID', ch_settings=ch_settings)   # Create staging table
    df_to_clickhouse(df=df, table_name=table_name, ch_settings=ch_settings) # Load staging df to staging table

    print("\nSuccess")

main(datestring='20240808', token=token)

