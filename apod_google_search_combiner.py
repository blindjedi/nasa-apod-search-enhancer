import os
import requests

from dotenv import load_dotenv

# Load environment variables from .env into the script's environment
load_dotenv()

# check if required environment variables are set
required_env_vars = ['nasa_api_key', 'google_api_key', 'search_engine_id']
for var_name in required_env_vars:
    if var_name not in os.environ:
        raise ValueError(f"Environment variable '{var_name}' is not set.")


def api_call(url: str, params: dict[str: str]) -> dict[str: any]:
    '''
        Resusable api call for nasa and google custom search api

    Parameters:
        url (str): The URL of the API endpoint.
        params (Dict[str, str]): A dictionary of query parameters to include in the request.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON response from the API.

    Raises:
        Exception: If the API request fails with a non-200 status code.
    '''
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f'Request failed with status code {response.status_code}', response.text)
