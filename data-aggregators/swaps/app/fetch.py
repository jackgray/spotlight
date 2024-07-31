import requests
from zipfile import ZipFile
from os import listdir, path, remove, makedirs
from io import BytesIO
from datetime import datetime, timedelta
# for parallel downloads
from concurrent.futures import ThreadPoolExecutor, as_completed

swaps_dir = '../data/sourcedata/swaps'
jurisdictions = ['SEC', 'CFTC']
report_types = ['SLICE', 'CUMULATIVE', 'FOREX', 'INTEREST']
asset_classes = ['CREDITS', 'EQUITIES', 'RATES']



def gen_url(jurisdiction, report_type, asset_class, datestring):
    dtcc_url = 'https://pddata.dtcc.com/ppd/api/report'
    return f'{dtcc_url}/{report_type.lower()}{jurisdiction.lower()}/{jurisdiction}_{report_type}_{asset_class}_{datestring}.zip'



def generate_date_strings(start_date, end_date):
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

def gen_urls(start_date, end_date, jurisdiction, report_type, asset_class):
    ''' 
        Returns array of formatted strings for URLs to DTCC swap data 

        Args:

        jurisdiction: one of 'SEC', 'CFTC'
        report type: one of 'SLICE', 'CUMULATIVE', FOREX, INTEREST
        asset classes: one of 'CREDITS', EQUITIES, 'RATES'    
    '''
    
    # Get an array of properly formatted datestrings for url
    date_strings = generate_date_strings(start_date, end_date)

    # Format the rest of the url for all dates
    urls = []
    for date in datestrings:
        url = gen_url(jurisdictioin, report_type, asset_class, date)
        urls.append(url)

    return urls



async def fetch_zip(url):
    ''' Downloads and returns zip byte stream from url '''
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            zipbytes = io.BytesIO(await response.read())
            return zipbytes



async def download_zip_to_df(url):
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


def process_file(urls):
    for url in urls
        df = await download_zip_to_df(url)
        df.append
    return dfs




async def batch():
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, url) for url in urls]
    for future in as_completed(futures)
        result = future.result()



asyncio.run(main())