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
# It is recommended to use environment variables to provision the credentials.
primero = PrimeroAPI(
    url='https://primero.example.com',
    username='primero',
    password='passw0rd!'
)

# Get cases
cases = primero.get_cases()

# Get incidents
incidents = primero.get_incidents()

# Get reports (as Report objects)
 
reports = primero.get_reports()

# Get the pandas version of the report table
reports[1].to_pandas()
```

### Interact with the reports
```python

report_id = 1
r = primero.get_report(report_id, lang='fr')

# Display the id
print('id', r.id)

# name of the report 
print('name', r.name, r.lang)

# raw data of the report as dict
print('raw_data', r.report_data_dict)

# pandas dataframe of the report
r.to_pandas()

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
Now you can edit the code ans see the results.

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


# LICENSE

MIT

