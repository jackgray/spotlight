import base64
import requests
import json
import csv
from io import StringIO
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os
import nasdaqdatalink
import pandas as pd

load_dotenv()
# Load environment variables
api_key = os.getenv('NASDAQ_API_KEY')

 
# data_feed = 'CFTC'
# codes_url = f'https://data.nasdaq.com/api/v3/datasets/{data_feed}/metadata.json?api_key={api_key}'
# response = requests.get(codes_url)
# print(response.headers.get('Content-Type'))
# data = StringIO(response.text)
# reader = csv.DictReader(data)
# print(list(reader))

def test():
    # Define the URL endpoint for searching datasets
    search_url = 'https://data.nasdaq.com/api/v3/datasets'

    # Define parameters for the search
    params = {
        'api_key': api_key,
        'database_code': 'CFTC',  # Example database code for CFTC datasets
        'per_page': 100,  # Number of datasets to retrieve per request
        'page': 1         # Start from the first page
    }

    all_datasets = []

    while True:
        response = requests.get(search_url, params=params)

        if response.status_code == 200:
            data = response.json()
            datasets = data['datasets']
            
            # Append the retrieved datasets to the list
            all_datasets.extend(datasets)
            
            # Check if there is another page of results
            if len(datasets) < params['per_page']:
                break
            else:
                params['page'] += 1
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break


    # Convert the list of datasets to a DataFrame
    df = pd.DataFrame(all_datasets)
    print(df)

test()
    
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
