from spotlight_utils.main import create_table_from_dict, df_to_clickhouse
from config import dtcc_source_schema, dtcc_source_schema2, ch_settings




async def main(datestring='20240101', dtcc_schema=dtcc_source_schema, dtcc_schema2=dtcc_source_schema2, ch_settings=ch_settings):

    print("Requesting swap records from DTCC for ", datestring)
    
    if int(datestring) > 20240126:  # The schema changes after Jan 26 2024
        table_name = "Swaps_DTCC_source2"
        schema_dict = dtcc_schema2
    else:
        table_name = "Swaps_DTCC_source"
        schema_dict = dtcc_schema

    url_datestring = '_'.join([datestring[:4], datestring[4:6], datestring[6:8]])   # Convert date into format url uses

    url = gen_dtcc_url('SEC', 'CUMULATIVE', 'EQUITIES', url_datestring) # This function can be used for pulling from cftc and other asset classes

    print(f"Retrieving {url}")
    df = fetch_zipped_csv(url=url)

    df['_RecordID'] = df['Dissemination Identifier'].astype(str) + df['Event timestamp'].astype(str).str.replace(r'[-:TZ]', '', regex=True)

    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('_-_','_').str.replace('-','_').str.replace('/','_')  # Remove spaces from column names
    df = df.astype(str)
    df.replace('nan', None, inplace=True)   # Ensure clickhouse handles null values properly
    df['_Report_Date'] = url_datestring          
    df['_Source_URL'] = url
    
    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='_RecordID', ch_settings=ch_settings)   # Create staging table
    try:
        df_to_clickhouse(df=origin_df, table_name=table_name, ch_settings=ch_settings) # Load staging df to staging table
        return df
        print("\nSuccess")
    except Exception as e:
        print(e)
        return e


def gen_dtcc_url(jurisdiction, report_type, asset_class, datestring):
    dtcc_url = 'https://pddata.dtcc.com/ppd/api/report'
    return f'{dtcc_url}/{report_type.lower()}/{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestring}.zip'
