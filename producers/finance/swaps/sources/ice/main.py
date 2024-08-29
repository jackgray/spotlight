from spotlight_utils.main import get_token, fetch_csv, create_table_from_dict, df_to_clickhouse, generate_datestrings
from config import ice_source_schema as schema_dict


def transform_df(df: pd.DataFrame, url: str) -> pd.DataFrame:

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
    df['_Source_URL'] = url

    return df


async def main(start_date='20240101', end_date='today', schema_dict=schema_dict, token=None, table_name='Swaps_ICE_source', ch_settings=ch_settings):
    ''' Grab record from ICE US SDR for a given date '''
    
    if token is None: # Get token if it wasn't provided
        token = await get_token("https://tradevault.ice.com/tvsec/ticker/webpi/getToken")

    datestrings = generate_datestrings(start_date='20240101', end_date='yesterday')

    urls=[]   # turn dates into urls to fetch in parallel
    for datestring in datestrings:
        url_datestring = '-'.join([datestring[:4], datestring[4:6], datestring[6:8]])   # Convert date into format url uses
        url = f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={url_datestring}'
        urls.append(url)

    await fetch_with_adaptive_concurrency(
        urls=urls,
        token=token,
        table_name=table_name,
        chunk_size=100000,
        transform_func=transform_df
    )



if __name__ == "__main__":
    asyncio.run(main(start_date='20240101', end_date='today', schema_dict=schema_dict, token=None, table_name='Swaps_ICE_source', ch_settings=ch_settings))
