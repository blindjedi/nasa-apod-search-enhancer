import pytest
from unittest.mock import patch

import apod_google_search_combiner


@patch('apod_google_search_combiner.requests.get')
def test_api_call_successful(mock_requests_get):
    '''
          Test successful API call handling for api_call().

        Expected Result: The api_call function should return a dictionary
    '''
    expected_response = {
        'title': 'Beautiful APOD Picture',
        'date': '2023-01-01',
        'explanation': 'This scene would be beautiful even without the comet.',
        'hdurl': 'https://apod.nasa.gov/apod/image',
        'media_type': 'image',
        'service_version': 'v1',
        'url': 'https://apod.nasa.gov/apod'

    }
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = expected_response

    nasa_apod_base_url = 'https://api.nasa.gov/planetary/apod'
    nasa_params = {'api_key': 'test_api_key'}

    result = apod_google_search_combiner.api_call(
        nasa_apod_base_url, nasa_params)

    assert result == expected_response
