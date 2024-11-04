import fsspec
from pandas import DataFrame
from dagster import asset, asset_check, OpExecutionContext, AssetCheckResult
from typing import Dict

from .resources import PrimeroAPIResource

@asset(description="Extracts all the cases from the primero instance. NO personal information is included in the output.")
def cases(context: OpExecutionContext, primero_api: PrimeroAPIResource) -> DataFrame:
    """ Retrieves cases from Primero API """

    # Check the version and connection to server is working
    context.log.info(f"Primero API library version {primero_api.version()}")
    context.log.info(f"Primero Server version {primero_api.get_server_version()}")

    context.log.info("Getting cases... ")
    df = primero_api.get_cases()
    #print(df)
    fs= fsspec.filesystem('s3')
    with fs.open('/primero/cases/cases.parquet','wb') as f:
        df.to_parquet(f)
    return df

#
# Asset checks allow to validate the data that is being produced by the asset
#
# https://docs.dagster.io/concepts/assets/asset-checks/define-execute-asset-checks
# https://docs.dagster.io/_apidocs/asset-checks#dagster.AssetCheckResult
#
@asset_check(asset=cases,
             description="Check if cases has at least one case")
def cases_num_check(cases: DataFrame) -> AssetCheckResult:
    rows = cases.shape[0]
    return AssetCheckResult(passed=rows > 1, metadata={"num_cases": rows})



@asset(description="Extracts all the incidents from the primero instance. NO personal information is included in the output.")
def incidents(context: OpExecutionContext, primero_api: PrimeroAPIResource) -> DataFrame:

    context.log.info("Getting incidents... ")
    # Get incidents method by default returns a PII free dataframe.
    # https://github.com/unicef/magasin-primero-paquet/tree/main/primero-api
    # In particular 
    # https://github.com/unicef/magasin-primero-paquet/tree/main/primero-api#interact-with-cases-and-the-incidents
    df = primero_api.get_incidents()

    fs= fsspec.filesystem('s3')
    with fs.open('/primero/incidents/incidents.parquet','wb') as f:
        df.to_parquet(f)
    return df


@asset_check(asset=incidents,
             description="Check if cases has at least one incident")
def incidents_num_check(incidents: DataFrame) -> AssetCheckResult:
    rows = incidents.shape[0]
    return AssetCheckResult(passed=rows > 1, metadata={"num_incidents": rows})


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