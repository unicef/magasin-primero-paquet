import fsspec
from pandas import DataFrame
from dagster import asset
from typing import Dict

from primero_api import PrimeroAPI

@asset
def cases() -> DataFrame:
  """ Retrieves cases from Primero API """
  # Load from API
  PRIMERO_USER= "primero"
  PRIMERO_PASSWORD='primer0!'
  PRIMERO_API_URL='http://localhost/api/v2/'

  print("Setting up connection to Primero API... ")
  primero = PrimeroAPI(PRIMERO_USER, PRIMERO_PASSWORD, PRIMERO_API_URL)
  print('Primero API library version', primero.version())
  print('Primero Server version', primero.get_server_version())

  print("Getting cases... ")
  df = primero.get_cases()
  print(df)
  fs= fsspec.filesystem('s3')
  with fs.open('/primero/cases/cases.parquet','wb') as f:
    df.to_parquet(f)
  return df


@asset
def incidents() -> DataFrame:
  """ Retrieves cases from Primero API """
  # Load from API
  PRIMERO_USER= "primero"
  PRIMERO_PASSWORD='primer0!'
  PRIMERO_API_URL='http://localhost/api/v2/'

  print("Setting up connection to Primero API... ")
  primero = PrimeroAPI(PRIMERO_USER, PRIMERO_PASSWORD, PRIMERO_API_URL)
  print('Primero API library version', primero.version())
  print('Primero Server version', primero.get_server_version())

  print("Getting cases... ")
  df = primero.get_incidents()
  print(df)
  fs= fsspec.filesystem('s3')
  with fs.open('/primero/cases/cases.parquet','wb') as f:
    df.to_parquet(f)
  return df



@asset
def reports()-> Dict:
  """ Retrieves reports from Primero API """

  # Load from API
  PRIMERO_USER= "primero"
  PRIMERO_PASSWORD='primer0!'
  PRIMERO_API_URL='http://localhost/api/v2/'

  primero = PrimeroAPI(PRIMERO_USER, PRIMERO_PASSWORD, PRIMERO_API_URL) 
  
  reports = primero.get_reports()

  fs= fsspec.filesystem('s3')
  for report in reports.values():  
    if report is None:
      continue
    with fs.open(f'/primero/report-{report.id}-{report.slug}/report.parquet','wb') as f:
      report.to_pandas().to_parquet(f)
    
  return reports