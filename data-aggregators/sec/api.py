import base64
import requests
import json
import csv
from io import StringIO
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os
import duckdb
import requests
import zipfile
import io
import csv
from bs4 import BeautifulSoup
import zipfile

load_dotenv()
# Load environment variables
api_key = os.getenv('FINRA_API_KEY')
api_secret = os.getenv('FINRA_API_SECRET')
data_dir = '..'
db_name = 'gme'
db_file = f'{data_dir}/{db_name}.duckdb'

url = 'https://www.sec.gov/files/data/{dataset}/cnsfails202406b.zip


# Define the URL of the ZIP file

headers = {'User-Agent': 'Your Name (your.email@example.com)'}

datasets = {
        'FTDs': {
            'scrape_url': 'https://www.sec.gov/data-research/sec-markets-data/foiadocsfailsdatahtm'
        }
    }


# Download and extract the ZIP file
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

downloads = []
table_rows = soup.select('table.views-table tbody tr')
for row in table_rows:
    link = row.find('a', href=True)
    if link:
        file_url = f'https://sec.gov/{link}'
        file_label = link['href'].split('/')[-1].replace('.zip', '')
        downloads.append((file_url, file_label))

# Connect to DuckDB and create the table
con = duckdb.connect(db_file)


try:
    last_download = con.execute(f'''
        SELECT file_label FROM {table_name}
        ORDER BY file_label DESC
        LIMIT 1
    ''').fetchone()
except Exception as e:
    print(e)
    print('Failed to retreive last entry for file_label. Table may not exist')

if file_label > last_download:
    response = requests.get(file_url, headers=headers)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    csv_filename = z.namelist()[0]
    print(f'Saving to file {csv_filename}')

    with z.open(csv_filename) as file:
        csv_reader = io.TextIOWrapper(file)
        for row in csv_reader:
            cols = row.strip().split(',')
            if cols[0].isdigit(): # skipping header
                con.execute(f'''
                    INSERT INTO {table_name}
                ''')

# Assuming the file we need is in the root of the ZIP
filename = z.namelist()[0]  # Update this based on the actual file name in the ZIP

# Extract the CSV file and read its content
with z.open(filename) as file:
    csv_reader = csv.reader(io.TextIOWrapper(file))

    # Connect to DuckDB and create the table
    con = duckdb.connect('sec_data.duckdb')
    con.execute('''
        CREATE TABLE fail_to_deliver (
            settlement_date INTEGER,
            cusip VARCHAR(9),
            symbol VARCHAR(10),
            quantity DOUBLE,
            description VARCHAR(30),
            price DOUBLE
        );
    ''')

    # Prepare to insert data
    insert_query = '''
        INSERT INTO fail_to_deliver (settlement_date, cusip, symbol, quantity, description, price)
        VALUES (?, ?, ?, ?, ?, ?);
    '''

    # Skip header row and insert data into DuckDB
    next(csv_reader)
    for row in csv_reader:
        con.execute(insert_query, [int(row[0]), row[1], row[2], float(row[3]), row[4], float(row[5])])

    # Commit and close the connection
    con.commit()
    con.close()

print("Data loaded successfully.")

def get_finra_session(api_key: str, api_secret: str) -> Optional[str]:
    """
    Retrieve a FINRA session token using the provided API key and secret.

    Parameters:
    api_key (str): The API key for FINRA.
    api_secret (str): The API secret for FINRA.

    Returns:
    Optional[str]: The FINRA session token if the request is successful, otherwise None.
    """

    # Encode the API key and secret
    finra_token = f"{api_key}:{api_secret}"
    encoded_token = base64.b64encode(finra_token.encode()).decode()

    # URL for requesting the session token
    url = "https://ews.fip.finra.org/fip/rest/ews/oauth2/access_token?grant_type=client_credentials"
    headers = {
        "Authorization": f"Basic {encoded_token}"
    }

    # Make the request to get the session token
    response = requests.post(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Failed to get session token: {response.status_code} {response.text}")
        return None


def fetch_finra(type: str, group: str, dataset:str) -> Optional[str]:
    """
    Query against FINRA Query API data from FINRA API.

    Args:
    type: 'metadata' or 'data'
    group: the category that the dataset belongs to. Examples: otcmarket, fixedincomemarket
    dataset: the name of the dataset you want. Examples: treasuryweeklyaggregates, weeklysummary

    More info here: https://developer.finra.org/docs#query_api-api_basics-api_request_types

    Returns:
    Optional[str, Any]: data if the request is successful, otherwise None.
    """

    # Generate session token
    token = get_finra_session(api_key, api_secret)
    if not token:
        return None
    else:
        # print(f'token: {token}')
        pass

    url = f"https://api.finra.org/{type}/group/{group}/name/{dataset}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response.raise_for_status()

        print(response.headers.get('Content-Type'))

        if response.headers.get('Content-Type') == 'text/plain':
            csv_data = StringIO(response.text)
            reader = csv.DictReader(csv_data)
            return list(reader)
        else:
            return response.json()
    else:
        print(f"Failed to fetch group {group} dataset {dataset}: {response.status_code} {response.text}")
        return None
