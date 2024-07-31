import requests
from zipfile import ZipFile
from os import listdir, path, remove, makedirs
from io import BytesIO
from datetime import datetime, timedelta
# for parallel downloads
from concurrent.futures import ThreadPoolExecutor, as_completed
from aiohttp import ClientSession
from argparse import ArgumentParser

swaps_dir = '../data/sourcedata/swaps'
jurisdictions = ['SEC', 'CFTC']
report_types = ['SLICE', 'CUMULATIVE', 'FOREX', 'INTEREST']
asset_classes = ['CREDITS', 'EQUITIES', 'RATES']



def gen_url(jurisdiction, report_type, asset_class, datestring):
    dtcc_url = 'https://pddata.dtcc.com/ppd/api/report'
    return f'{dtcc_url}/{report_type.lower()}{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestring}.zip'



def generate_date_strings(start_date, end_date):
    '''
        Input date must be in format YYYYmmdd aka 20240130 for jan 30 2024
    '''
    date_format = '%Y%m%d'
    try:
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return []
    date_strings = []
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y_%m_%d')
        date_strings.append(date_str)
        current_date += timedelta(days=1)
    return date_strings

def gen_urls(start_date: str, end_date: str, jurisdiction: str, report_type: str, asset_class: str) -> list[str]:
    ''' 
        Returns array of formatted strings for URLs to DTCC swap data 

        Args:

        jurisdiction: one of 'SEC', 'CFTC'
        report type: one of 'SLICE', 'CUMULATIVE', FOREX, INTEREST
        asset classes: one of 'CREDITS', EQUITIES, 'RATES'    
    '''
    
    # Get an array of properly formatted date strings for url
    dates = generate_date_strings(start_date, end_date)

    # Format the rest of the url for all dates
    urls = []
    for date in dates:
        url = gen_url(jurisdiction, report_type, asset_class, date)
        urls.append(url)

    return urls



async def fetch_zip(session: ClientSession, url: str) -> BytesIO:
    ''' Downloads and returns zip byte stream from url '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            zipbytes = BytesIO(await response.read())
            return zipbytes



async def download_zip_to_df(session: ClientSession, url: str) -> pl.DataFrame:
    '''
        Returns a dataframe after downloading zipfile from a source
        without needing to save to disk

        Can be useful for saving raw data directly to duckdb, parquet, 
        or more efficient format or to remote storage rather than csv on local disk as an extra step
    '''
    # Download zip file to memory
    zipbytes = await fetch_zip()

    with ZipFile(zipbytes, 'r') as ref:
        csv = ref.namelist()[0]
        with ref.open(csv) as file:
            df = pl.read_csv(file)
    
    return df


async def process_urls(urls: list[str]) -> list[pl.DataFrame]:
    async with aiohttp.ClientSession() as session:
        tasks = [download_zip_to_df(session, url) for url in urls]
        dfs = await asyncio.gather(*tasks, return_exceptions=True)
        return dfs



def main(start_date: str, end_date: str, jurisdiction: str, report_type: str, asset_class: str):
    urls = gen_urls(start_date, end_date, jurisdiction, report_type, asset_class)
    loop = asyncio.get_event_loop()
    dfs = loop.run_until_complete(process_urls(urls))
    for df in dfs:
        if isinstance(df, Exception):
            print(f"Error: {df}")
        else:
            print(df)

if __name__ == "__main__":
    parser = ArgumentParser(description='Download and process zip files.')
    parser.add_argument('start_date', type=str, help='Start date in YYYYmmdd format')
    parser.add_argument('end_date', type=str, help='End date in YYYYmmdd format')
    parser.add_argument('jurisdiction', type=str, choices=jurisdictions, help='Jurisdiction (SEC or CFTC)')
    parser.add_argument('report_type', type=str, choices=report_types, help='Report type')
    parser.add_argument('asset_class', type=str, choices=asset_classes, help='Asset class')
    
    args = parser.parse_args()

    main(args.start_date, args.end_date, args.jurisdiction, args.report_type, args.asset_class))
