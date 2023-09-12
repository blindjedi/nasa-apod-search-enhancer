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


@patch('apod_google_search_combiner.requests.get')
def test_api_call_failure(mock_requests_get):
    '''
    Test failure API call handling for api_call().

    Expected Result: The api_call function should raise an Exception for non 200 status code
    '''
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 404
    mock_response.text = 'Site Not Found'

    with pytest.raises(Exception) as exception:
        nasa_apod_base_url = 'https://api.nasa.gov/planetary/apod'
        nasa_params = {'api_key': 'test_api_key'}
        apod_google_search_combiner.api_call(nasa_apod_base_url, nasa_params)

    assert 'Request failed with status code 404' in str(exception.value)
    assert 'Site Not Found' in str(exception.value)


def test_combine_results():
    '''
    Test the combine_results function with sample APOD and Google search data.

    Expected_result: combine_results should return a dictionary 
    '''
    apod_data = {
        'title': 'Beautiful APOD Picture',
        'date': '2023-01-01',
        'explanation': 'This scene would be beautiful even without the comet.',
        'hdurl': 'https://apod.nasa.gov/apod/image',
        'media_type': 'image',
        'service_version': 'v1',
        'url': 'https://apod.nasa.gov/apod'

    }
    google_search_data = {
        'queries': {'request': [{}]},
        'context': {'title': 'Beautiful APOD Picture'},
        'items': [
            {'link': ''},
            {'link': ''}
        ],
        'url': ''
    }

    expected_result = {
        'apod_data': apod_data,
        'google_search_data': google_search_data['items']
    }

    result = apod_google_search_combiner.combine_results(
        apod_data, google_search_data)

    assert result == expected_result
