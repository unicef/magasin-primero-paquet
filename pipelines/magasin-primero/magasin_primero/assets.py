import fsspec
from pandas import DataFrame
from dagster import asset, OpExecutionContext
from typing import Dict

from primero_api import PrimeroAPI

@asset
def cases(context: OpExecutionContext) -> DataFrame:
  """ Retrieves cases from Primero API """
  # Load from API
  PRIMERO_USER= "primero"
  PRIMERO_PASSWORD='primer0!'
  PRIMERO_API_URL='http://localhost/api/v2/'

  primero = PrimeroAPI(PRIMERO_USER, PRIMERO_PASSWORD, PRIMERO_API_URL)
  # Check the version and connection to server is working
  context.log.info(f"Primero API library version {primero.version()}")
  context.log.info(f"Primero Server version {primero.get_server_version()}")

  context.log.info("Getting cases... ")
  df = primero.get_cases()
  print(df)
  fs= fsspec.filesystem('s3')
  with fs.open('/primero/cases/cases.parquet','wb') as f:
    df.to_parquet(f)
  return df


@asset
def incidents(context: OpExecutionContext) -> DataFrame:
  """ Retrieves incidents from Primero API """
  # Load from API
  PRIMERO_USER= "primero"
  PRIMERO_PASSWORD="primer0!"
  PRIMERO_API_URL="http://localhost/api/v2/"


  primero = PrimeroAPI(PRIMERO_USER, PRIMERO_PASSWORD, PRIMERO_API_URL)
  context.log.info("Getting incidents... ")
  df = primero.get_incidents()
  print(df)
  fs= fsspec.filesystem('s3')
  with fs.open('/primero/incidents/incidents.parquet','wb') as f:
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