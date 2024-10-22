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
  PRIMERO_API_URL='http://localhost/api/v2'

  print("Setting up connection to Primero API... ")
  primero = PrimeroAPI(PRIMERO_USER, PRIMERO_PASSWORD, PRIMERO_API_URL) 
  
  print("Getting cases... ")
  df = primero.get_cases()
  print("------ cases ------")
  print(df)
  print("------ cases ------")
  
  fs= fsspec.filesystem('s3')
  with fs.open('/primero/cases.parquet','wb') as f:
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
  fs= fsspec.filesystem('s3')
  
  reports = primero.get_reports()
  for report in reports:  
    with fs.open(f'/primero/report-{report.id}-{report.slug}.parquet','wb') as f:
      report.to_pandas().to_parquet(f)
    
  return reports