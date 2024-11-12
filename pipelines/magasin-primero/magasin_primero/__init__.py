import os 

from dagster import Definitions, load_assets_from_modules, EnvVar
from .resources import PrimeroAPIResource
from . import assets
from dagster import load_asset_checks_from_modules
from dagster import ScheduleDefinition, DefaultScheduleStatus, AssetSelection
from .version import __version__, print_cool_banner


# This will displayed on the logs of the pod when loaded
environment = os.getenv("ENVIRONMENT")
print_cool_banner()
print('-------------------------------------------------')
print(f'Pipeline Version: {__version__}')
print(f'ENVIRONMENT={environment}')
print('-------------------------------------------------')

# Load all assets from the assets module
all_assets = load_assets_from_modules([assets], group_name="primero")

all_asset_checks = load_asset_checks_from_modules([assets])

# Load from env the primero settings
primero_user = EnvVar("PRIMERO_USER")
primero_password = EnvVar("PRIMERO_PASSWORD")
primero_api_url = EnvVar("PRIMERO_API_URL") # Should end with /

# Create the API client resource 
primero_api_resource = PrimeroAPIResource(primero_user=primero_user,
                                          primero_password=primero_password,
                                          primero_api_url=primero_api_url)

# Default schedule for the job every day at midnight
schedule = ScheduleDefinition(
    name="daily_job",
    target=all_assets,
    cron_schedule="0 0 * * *",
    default_status= DefaultScheduleStatus.RUNNING)

if environment == 'dev':
    schedule = ScheduleDefinition(
    name="dev_minute_job",
    target=all_assets,
    cron_schedule="* * * * *",
    #default_status= DefaultScheduleStatus.RUNNING
    )


defs = Definitions(
    assets=all_assets,
    asset_checks=all_asset_checks,
    schedules=[schedule],
    resources={"primero_api": primero_api_resource}
)
