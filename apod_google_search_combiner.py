import os
import logging
import requests

from dotenv import load_dotenv
from typing import Dict, Any

log = logging.getLogger('nasa_apod_search_enhancer')
log.setLevel(logging.INFO)


# Load environment variables from .env into the script's environment
load_dotenv()

# check if required environment variables are set
required_env_vars = ['nasa_api_key', 'google_api_key', 'search_engine_id']
for var_name in required_env_vars:
    if var_name not in os.environ:
        raise ValueError(f"Environment variable '{var_name}' is not set.")


def api_call(url: str, params: Dict[str, str]) -> Dict[str, Any]:
    '''
    Resusable GET api call for nasa and google custom search api

    Parameters:
        url (str): The URL of the API endpoint.
        params (Dict[str, str]): A dictionary of query parameters to include in the request.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON response from the API.

    Raises:
        Exception: If the API request fails with a non-200 status code.
    '''
    log.info(f'Sending Get request for url: {url}')
    response = requests.get(url, params=params)
    if response.status_code == 200:
        log.info(f'Successful GET Request for url: {url}')
        return response.json()
    else:
        log.error(f'Error during GET request for url: {url}')
        raise requests.exceptions.HTTPError(
            f'HTTP error {response.status_code}: {response.text}, for request {url}'
        )


def validate_apod_data(apod_data: Dict[str, str]) -> bool:
    '''
    This function checks whether the provided APOD data dictionary contains
    the expected keys ('title', 'url', 'date', and 'explanation') and whether
    the values for these keys are non-empty strings.
    '''
    expected_keys = ['title', 'url', 'date', 'explanation']

    # Check if all expected keys are present
    if not all(key in apod_data for key in expected_keys):
        return False

    # Check if the values for these keys are non-empty strings
    for key in expected_keys:
        value = apod_data[key]
        if not isinstance(value, str) or not value.strip():
            return False

    return True
    '''
    Combines data from the NASA Astronomy Picture of the Day (APOD) API
    and Google Custom Search API into a single dictionary.

    Parameters:
        apod_data (dict[str, Any]): Data from the APOD API.
        google_search_data (dict[str, Any]): Data from the Google Custom Search API.

    Returns:
        dict[str, Any]: A dictionary containing combined information.
    '''
    return {
        'apod_data': apod_data,
        'google_search_data': google_search_data['items']
    }


if __name__ == '__main__':
    # NASA APOD API Call
    nasa_apod_base_url = 'https://api.nasa.gov/planetary/apod'
    nasa_params = {
        'api_key': os.environ['nasa_api_key']
    }
    apod_data = api_call(nasa_apod_base_url, nasa_params)

    # Google Search API Call using APOD title
    google_custom_search_base_url = 'https://www.googleapis.com/customsearch/v1'
    google_params = {
        'key': os.environ['google_api_key'],
        'cx': os.environ['search_engine_id'],
        'q': apod_data['title']
    }
    google_search_data = api_call(google_custom_search_base_url, google_params)

    apod_with_additional_info = combine_results(apod_data, google_search_data)

    print(
        f'apod with additional google search results: \n{apod_with_additional_info}'
    )
