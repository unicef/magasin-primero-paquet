# Primero API Python library (primero-api) [Experimental]

This is a python library to interact with the [Primero IMS](primero.org) API.

This library is part of the magasin-primero-paquet project.

It's main goal is to enable data analysts to extract data programmatically from a Primero instance either for performing exploratory analysis or building a data pipeline. 

Tested with primero `2.11.0-rc3`.

## Installation

```shell
pip install primero-api
```

## Usage

```python
from primero_api import PrimeroAPI

# Initialize the API client
# Replace the url, username and password with your own.
primero = PrimeroAPI(
    url='https://primero.example.com/api/v2/',
    username='primero',
    password='passw0rd!'
)
# Test the api connection
print(primero.get_server_version())
# '2.11.0-rc3'
```

In a production environment, it is recommended to use [environment variables](https://en.wikipedia.org/wiki/Environment_variable) to provide the credentials.

```sh
export PRIMERO_USER='primero'
export PRIMERO_PASSWORD='primer0!'
export PRIMERO_API_URL='http://localhost/api/v2/'
```

Then you can use the following code to read the environment variables.

```python
import os

PRIMERO_USER= os.getenv('PRIMERO_USER')
PRIMERO_PASSWORD= os.getenv('PRIMERO_PASSWORD')
PRIMERO_API_URL= os.getenv('PRIMERO_API_URL')

primero = PrimeroAPI(
    url=PRIMERO_API_URL,
    username=PRIMERO_USER,
    password=PRIMERO_PASSWORD
)

```

### Interact with cases and the incidents
The API client, is mainly focused on data analysis so it basically provides a few methods to extract data from a Primero instance.

```python

# Get cases
cases = primero.get_cases()

# Get incidents
incidents = primero.get_incidents()
```

By default the client will return the data in a pandas DataFrame format and by default data is ANONYMIZED, that is only a subset of the information stored in the case and incident is processed.
This is done to protect the privacy of the individuals in the system and prevent the leakage of sensitive information.

If there is some data that you need for your use case, you can use `additional_fields` to be included as part of the data.

```python

# Get cases with anonymization disabled, this will return all the fields in the case
cases = primero.get_cases(additional_fields=['name','date_of_birth'])
incidents = primero.get_incidents(additional_fields=['name','date_of_birth'])
```

You can even fully disable the anonymization by setting `anonymize=False` in the `get_cases` method.

```python
cases = primero.get_cases(anonymize=False)
incidents = primero.get_incidents(anonymize=False)
```



Lastly, you can also get the raw data as a dictionary:

```python
# Get cases as returned by the API
cases = primero.get_cases_raw()

# Get incidents
incidents = primero.get_incidents_raw()
```


### Interact with the reports

```python

# Dictionary of reports in which the key is the id of the report
reports = primero.get_reports()

# Display the report id, name and language
for report in reports.values():
  print(report.id, report.name, report.lang, report.slug)
```

You can also get a report by its id

```python
report = primero.get_report(1) # where 1 is the id of the report
print(report.id, report.name, report.lang, report.slug)
```

Get the data of a report
```python
report = primero.get_report(1) # where 1 is the id of the report

# Get the data of the report as a pandas DataFrame
# This will process the original data and return it as a pandas DataFrame with the rows and columns
report_df =  report.to_pandas()
print(report_df)

# Get the raw data of the report as a dictionary
# This is the original data as returned by the API without any processing
print(report.report_data_dict)

```


## Development

Get the repo

```shell
git clone https://github.com/unicef/magasin-primero-paquet  
```
Go to the library folder

```shell
cd primero-magasin-paquet
cd primero_api
```
Install in edit mode

```shell
pip install -e ".[dev]"
```
Now you can edit the code and see the results when you run test code.

## Unit Testing

To run the unit tests:
```
pytest tests
```

## Integration testing

To run the integration tests, you need to have a running primero instance running and set the environment variables below. 

```
export PRIMERO_USER='primero'
export PRIMERO_PASSWORD='primer0!'
export PRIMERO_API_URL='http://localhost/api/v2/'
```

If the environment variables are not set, the tests will use the default values:

```
PRIMERO_USER='primero'
PRIMERO_PASSWORD='primer0!'
PRIMERO_API_URL='http://localhost/api/v2/'
```

```shell
pytest integration_tests
```

### Integration testing with environment file

Optionally, you can use a file to set these variables. Follow these steps: 

1. Create a copy the example file:
    ```
    cp integration_env.conf-sample integration_env.conf
    ```
2. Then update the values in `integration_env.conf` with your own values.

3. Run:

```shell
source integration_env.conf
pytest integration_tests
```

### All tests with code coverage

To run all the tests:

```shell
pytest --cov=primero_api 
```


## LICENSE

MIT

