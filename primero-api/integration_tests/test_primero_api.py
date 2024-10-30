# These tests an actual API call to an actual server
import os
import pytest 
from pandas import DataFrame
from primero_api import PrimeroAPI, Report

# Load from environment variables
PRIMERO_USER = os.getenv('PRIMERO_USER', 'primero')
PRIMERO_PASSWORD = os.getenv('PRIMERO_PASSWORD', 'primer0!')
PRIMERO_API_URL= os.getenv('PRIMERO_API_URL', 'http://localhost/api/v2/')


def test_constructor():
    primero = PrimeroAPI(user=PRIMERO_USER, password=PRIMERO_PASSWORD, api_url=PRIMERO_API_URL)
    assert primero is not None

def test_constructor_with_params():
    primero = PrimeroAPI(user=PRIMERO_USER, password=PRIMERO_PASSWORD, api_url=PRIMERO_API_URL, page_size=1, rate=2, duration=1, cache_expire=1)
    assert primero is not None

@pytest.fixture
def primero_api():
   return PrimeroAPI(user=PRIMERO_USER, password=PRIMERO_PASSWORD, api_url=PRIMERO_API_URL, page_size=1, rate=2, duration=1, cache_expire=1)

def test_get_cases_raw(primero_api):
    cases = primero_api.get_cases_raw()
    assert cases is not None
    assert type(cases) is list
    assert cases[0] is not None

def test_get_cases(primero_api):
    cases = primero_api.get_cases()
    assert cases is not None
    assert type(cases) is DataFrame

def test_get_cases_anonymized_false(primero_api):
    cases = primero_api.get_cases(anonymized=False)
    assert cases is not None
    assert type(cases) is DataFrame
    


def test_get_incidents_raw(primero_api):
    incidents = primero_api.get_incidents_raw()
    assert incidents is not None
    assert type(incidents) is list

def test_get_incidents(primero_api):
    incidents = primero_api.get_incidents()
    assert incidents is not None
    # asset is a DataFrame
    assert type(incidents) is DataFrame

def test_get_reports(primero_api):
    reports = primero_api.get_reports()
    assert reports is not None
    assert type(reports) is dict 


def test_get_report(primero_api):
    report = primero_api.get_report(1)
    assert report is not None
    # check is a Report object
    assert type(report) is Report
    assert report.id == 1
    assert type(report.name) == str
    assert type(report.description) == str
    assert type(report.slug) == str
    assert type(report.to_pandas()) == DataFrame
    assert type(report.labels()) == dict

def test_get_version(primero_api):
    version = primero_api.get_server_version()
    # check is a string
    assert type(version) is str
