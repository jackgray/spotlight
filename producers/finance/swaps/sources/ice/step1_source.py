
from spotlight_utils.main import get_token, fetch_csv, create_table_from_dict, df_to_clickhouse
from config import ice_source_schema as schema_dict


token = get_token("https://tradevault.ice.com/tvsec/ticker/webpi/getToken") # This should just be run once at the beginning of a 

def main(datestring=20240101, ice_schema=ice_source_schema, token=None, table_name='Swaps_ICE_source', ch_settings=ch_settings):
    ''' Grab record from ICE US SDR for a given date '''
    
    url_datestring = '-'.join([datestring[:4], datestring[4:6], datestring[6:8]])   # Convert date into format url uses
    url = f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={url_datestring}'

    print("\nRequesting record from ICE: ", url)
    df = fetch_csv(url=url, token=token)

    df['_RecordID'] = df['Dissemination identifier'] + df['Event timestamp'].astype(str).str.replace(r'[-:TZ]', '', regex=True)
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('_-_','_').str.replace('-','_').str.replace('/','_')  # Remove spaces from column names
    df = df.astype(str)
    df.replace('nan', None, inplace=True)   # Ensure clickhouse handles null values properly
    df['_Report_Date'] = url_datestring          
    df['_Source_URL'] = url

    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='_RecordID', ch_settings=ch_settings)   # Create staging table
    df_to_clickhouse(df=origin_df, table_name=table_name, ch_settings=ch_settings) # Load staging df to staging table

    print("\nSuccess")
