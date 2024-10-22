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

```shell
pytest tests 
```

## Integration testing

To run the unit tests:
```
pytest tests
```

To run the integration tests, you need to have a running primero instance and the environment variables below. It will use the following default values

```
PRIMERO_USER='primero'
PRIMERO_PASSWORD='primer0!'
PRIMERO_API_URL='http://localhost/api/v2/'
```

After setting the environment variables, run the integration tests:

```shell
pytest integration_tests
```

You can also create a file `integration_env.conf` with the following content:

```
cp integration_env.conf-sample integration_env.conf
```

Then update the values in `integration_env.conf` with your own values and run:


```shell
source integration_env.conf
pytest integration_tests
```


# LICENSE

MIT

