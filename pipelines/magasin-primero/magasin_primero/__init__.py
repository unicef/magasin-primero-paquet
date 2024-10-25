from dagster import Definitions, load_assets_from_modules, EnvVar
from .resources import PrimeroAPIResource
from . import assets

# Load all assets from the assets module
all_assets = load_assets_from_modules([assets], group_name="primero")

# Load from env the primero settings
primero_user = EnvVar("PRIMERO_USER")
primero_password = EnvVar("PRIMERO_PASSWORD")
primero_api_url = EnvVar("PRIMERO_API_URL") # Should end with /

# Create the API client resource 
primero_api_resource = PrimeroAPIResource(primero_user=primero_user,
                                          primero_password=primero_password,
                                          primero_api_url=primero_api_url)

defs = Definitions(
    assets=all_assets,
    resources={"primero_api": primero_api_resource}
)
