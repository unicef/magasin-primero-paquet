import pytest

from primero_api import PrimeroAPI
import requests_mock


@pytest.fixture
def primero_api():
    return PrimeroAPI(user='test_user', password='test_password', api_url='http://test.api/', page_size=2)

def test_is_last_page(primero_api):
    # Test data for is_last_page
    metadata_last_page = {
        'page': 2,
        'total': 20,
        'per': 10
    }
    assert primero_api._is_last_page(metadata_last_page) == True

    metadata_not_last_page = {
        'page': 1,
        'total': 20,
        'per': 10
    }
    assert primero_api._is_last_page(metadata_not_last_page) == False


def test_call_paginated_api(primero_api):
    # Mock the responses for the paginated API calls
    # Test data for call_paginated_api
    response_data_page_1 = {
        'data': [{'id': 1}, {'id': 2}],
        'metadata': {'page': 1, 'total': 4, 'per': 2}
    }
    response_data_page_2 = {
        'data': [{'id': 3}, {'id': 4}],
        'metadata': {'page': 2, 'total': 4, 'per': 2}
    }

    with requests_mock.Mocker() as m:
        m.get('http://test.api/?per=2&page=1', json=response_data_page_1)
        m.get('http://test.api/?per=2&page=2', json=response_data_page_2)
        data = primero_api._call_paginated_api('http://test.api/')
    
        assert len(data) == 4
        assert data == [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}]


def test_remove_record_pii_default(primero_api):
    record_with_pii = {
        'name': 'John Doe', # PII 
        'date_of_birth': 'john.doe@example.com', # PII
        'address_current': '123 Main St', # PII
        'enabled': 'non_pii_value' # Non-PII
    }
    result_record_without_pii = {
        'enabled': 'non_pii_value'
    }

    result = primero_api._remove_record_pii(record_with_pii)
    assert result == result_record_without_pii

def test_remove_record_pii_custom_cols(primero_api):
    record_with_custom_non_pii = {
        'name': 'John Doe', # PII 
        'date_of_birth': 'john.doe@example.com', # PII
        'address_current': '123 Main St', # PII
        'enabled': 'non_pii_value', # Non-PII
        'custom_non_pii': 'custom_value'
    }

    result_record_with_custom_non_pii = {
        'enabled': 'non_pii_value', # Non-PII
        'custom_non_pii': 'custom_value' # Additional non-PII
    }

    result = primero_api._remove_record_pii(record_with_custom_non_pii, additional_non_pii_cols=['custom_non_pii'])
    assert result == result_record_with_custom_non_pii

def test_remove_record_pii_custom_nonexistent_cols(primero_api):
    
    record_with_custom_non_pii = {
        'name': 'John Doe', # PII 
        'date_of_birth': 'john.doe@example.com', # PII
        'address_current': '123 Main St', # PII
        'enabled': 'non_pii_value', # Non-PII
        'custom_non_pii': 'custom_value'
    }

    result_record_with_custom_nonexistent_pii = {
        'enabled': 'non_pii_value', # Non-PII
    }
    # the additional_non_pii_cols do not exist and still does not break
    result = primero_api._remove_record_pii(record_with_custom_non_pii, additional_non_pii_cols=['nonexistent_col'])
    assert result == result_record_with_custom_nonexistent_pii

def test_remove_record_pii_with_modified_non_pii_cols(primero_api):
    record_with_pii = {
        'name': 'John Doe', # PII 
        'date_of_birth': 'john.doe@example.com', # PII
        'address_current': '123 Main St', # PII
        'enabled': 'non_pii_value' # Non-PII
    }
    # Now I am going to white list name, date_of_birth, and address_current
    # so only enabled is considered PII
    primero_api.set_non_pii_cols(['name', 'date_of_birth', 'address_current'])
    
    result_record_without_pii = {
        'name': 'John Doe', # PII 
        'date_of_birth': 'john.doe@example.com', # PII
        'address_current': '123 Main St', # PII
    }
    result = primero_api._remove_record_pii(record_with_pii)
    assert result == result_record_without_pii