from dagster import ConfigurableResource, InitResourceContext
from primero_api import PrimeroAPI


class PrimeroAPIResource(ConfigurableResource):
    """
    This is just a wrapper of the PrimeroAPI class as a Pythonic resource

    See: https://github.com/unicef/magasin-primero-paquet/tree/main/primero-api
    See: https://docs.dagster.io/_apidocs/resources
    """
    primero_user: str
    primero_password: str
    primero_api_url: str

    # These are optional values for the PrimeroAPI constructor.
    # In create_resource they are only passed to the PrimeroAPI constructor if they're set when initializing the PrimeroAPIResource. 
    # Otherwise it will use the ones provided by the library

    page_size: int = None
    rate: int = None
    duration: int = None
    cache_expire: int = None

    def create_resource(self, context: InitResourceContext) -> PrimeroAPI:
        """
        Returns a PrimeroAPI resource.
        Returns:
            PrimeroAPI: An instance of the PrimeroAPI class initialized with the provided user, password, api_url, 
                page_size, rate, duration, and cache_expire attributes.
        """
        kwargs = {
            'user': self.primero_user,
            'password': self.primero_password,
            'api_url': self.primero_api_url
        }
        
        if self.page_size is not None:
            kwargs['page_size'] = self.page_size
        if self.rate is not None:
            kwargs['rate'] = self.rate
        if self.duration is not None:
            kwargs['duration'] = self.duration
        if self.cache_expire is not None:
            kwargs['cache_expire'] = self.cache_expire

        return PrimeroAPI(**kwargs)
