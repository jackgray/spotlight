import base64
import requests
import json
import csv
from io import StringIO
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os


load_dotenv()
# Load environment variables
api_key = os.getenv('FINRA_API_KEY')
api_secret = os.getenv('FINRA_API_SECRET')

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