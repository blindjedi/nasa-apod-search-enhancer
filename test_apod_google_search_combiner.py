import pytest
import requests
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

    with pytest.raises(requests.exceptions.HTTPError) as exception:
        nasa_apod_base_url = 'https://api.nasa.gov/planetary/apod'
        nasa_params = {'api_key': 'test_api_key'}
        apod_google_search_combiner.api_call(
            nasa_apod_base_url, nasa_params)

    assert 'HTTP error 404: Site Not Found, for request https://api.nasa.gov/planetary/apod' in str(
        exception.value)


def test_validate_apod_data_success():
    '''
    Test the success case of the validate_apod_data function.

    Expected Result:
    The validate_apod_data function should return True when provided with
    valid APOD data.
    '''
    data = {
        'title': 'Galaxy Cluster Abell 370 and Beyond',
        'url': 'https://apod.nasa.gov/apod/image/2309/STSCI-HST-abell370_1024.jpg',
        'date': '2023-09-12',
        'explanation': "Some 4 billion light-years away, massive galaxy cluster Abell 370..."
    }

    result = apod_google_search_combiner.validate_apod_data(data)

    assert result is True


def test_validate_apod_data_failure():
    '''
    Test the failure case of the validate_apod_data function.

    Expected Result:
    The validate_apod_data function should return False when provided with
    invalid APOD data.
    '''
    invalid_data = {
        'title': 'Invalid APOD',
        'url': '',
        'date': '2023-09-12',
        'explanation': ''
    }

    result = apod_google_search_combiner.validate_apod_data(invalid_data)

    assert result is False


def test_validate_google_search_data_success():
    """
    This test case validates that the function correctly handles valid Google search data.

    Expected Result:
    The validate_google_search_data function should return True when provided with
    valid Google search data containing 'items'.
    """
    valid_data = {
        'kind': 'customsearch#search',
        'items': [{'title': 'Result 1'}, {'title': 'Result 2'}]
    }

    assert apod_google_search_combiner.validate_google_search_data(
        valid_data) is True


def test_validate_google_search_data_failure():
    """
    This test case validates that the function correctly detects invalid Google search data.

    Expected Result:
    The validate_google_search_data function should return False when provided with
    invalid Google search data that lacks 'items'.
    """
    invalid_data = {
        'kind': 'customsearch#search',
        'items': []
    }

    assert apod_google_search_combiner.validate_google_search_data(
        invalid_data) is False


def test_combine_results_valid_google_data():
    """
    This test case validates that the function correctly combines APOD and valid Google search data.

    Expected Result:
    The combine_results function should return a dictionary with 'apod_data' and 'google_search_data'.
    'google_search_data' should be a list of items from valid Google search data.
    """
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
        'kind': 'customsearch#search',
        'queries': {'request': [{}]},
        'context': {'title': 'Beautiful APOD Picture'},
        'items': [
            {'title': 'Result 1'},
            {'title': 'Result 2'}
        ]
    }

    is_valid_google_data = True

    result = apod_google_search_combiner.combine_results(
        apod_data, google_search_data, is_valid_google_data)

    assert result['apod_data'] == apod_data
    assert len(result['google_search_data']) == 2


def test_combine_results_invalid_google_data():
    """
    This test case validates that the function correctly combines APOD data and handles invalid Google search data.

    Expected Result:
    The combine_results function should return a dictionary with 'apod_data' and a message indicating
    that no Google search results were found.
    """
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
        'kind': 'customsearch#search',
        'items': []
    }

    is_valid_google_data = False

    result = apod_google_search_combiner.combine_results(
        apod_data, google_search_data, is_valid_google_data)

    assert result['google_search_data'] == 'No Google Search Results Found'
    assert result['apod_data'] == apod_data

