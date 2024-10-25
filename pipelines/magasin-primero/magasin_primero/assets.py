import fsspec
from pandas import DataFrame
from dagster import asset, OpExecutionContext
from typing import Dict

from primero_api import PrimeroAPI

from .resources import PrimeroAPIResource

@asset
def cases(context: OpExecutionContext, primero_api: PrimeroAPIResource) -> DataFrame:
    """ Retrieves cases from Primero API """

    # Check the version and connection to server is working
    context.log.info(f"Primero API library version {primero_api.version()}")
    context.log.info(f"Primero Server version {primero_api.get_server_version()}")

    context.log.info("Getting cases... ")
    df = primero_api.get_cases()
    print(df)
    fs= fsspec.filesystem('s3')
    with fs.open('/primero/cases/cases.parquet','wb') as f:
        df.to_parquet(f)
    return df


@asset
def incidents(context: OpExecutionContext, primero_api: PrimeroAPIResource) -> DataFrame:
    """ Retrieves incidents from Primero API saves them in storage"""
    context.log.info("Getting incidents... ")
    df = primero_api.get_incidents()

    fs= fsspec.filesystem('s3')
    with fs.open('/primero/incidents/incidents.parquet','wb') as f:
        df.to_parquet(f)
    return df



@asset
def reports(context: OpExecutionContext, primero_api: PrimeroAPIResource)-> Dict:
    """ Retrieves reports from Primero API """

    context.log.info("Getting reports... ")
    reports = primero_api.get_reports()

    fs= fsspec.filesystem('s3')
    for report in reports.values():  
        if report is None:
            continue
        with fs.open(f'/primero/report-{report.id}-{report.slug}/report.parquet','wb') as f:
        report.to_pandas().to_parquet(f)
        
    return reports