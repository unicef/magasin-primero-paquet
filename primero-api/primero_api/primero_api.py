import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# To Limit the requests to prevent hitting the rate limit
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

from typing import List

from .logger import logger

from .report import Report
from .version import get_version

NON_PII_COLS = ['enabled',
                'age',
                'sex',
                'status',
                'flagged',
                'owned_by',
                'workflow',
                'estimated',
                'has_photo',
                'module_id',
                'record_state',
                'has_case_plan',
                'has_incidents',
                'reopened_logs',
                'followup_dates',
                'case_id_display',
                'created_at'
                'last_updated_at',
                'last_updated_by',
                'maritial_status',
                'owned_by_groups',
                'closure_approved',
                'location_current',
                #'consent_reporting', # --- error in to-parquet conversion
                'interview_subject',
                'registration_date',
                'case_plan_approved',
                'owned_by_agency_id',
                'assessment_approved',
                'assessment_due_date',
                'current_alert_types',
                'not_edited_by_owner',
                'protection_concerns',
                #'address_is_permanent',
                'case_status_reopened',
                'consent_for_services',
                'created_organization',
                'transferred_to_users',
                'associated_user_names',
                'disclosure_other_orgs',
                'referred_users_present',
                'withholding_info_reason',
                #'followup_subform_section', # -- gives error in to parquet conversion
                'transferred_to_user_groups',
                'service_implemented_day_times',
                'record_in_scope',
                'flag_count',
                'alert_count',
                'current_care_arrangements_type',
                'current_care_arrangement_started_date'
                ]


class CachedLimiterSession(CacheMixin, LimiterMixin, requests.Session):
    pass


class PrimeroAPI:

    def __init__(self, user, password, api_url, page_size=1000, rate=2, duration=1, cache_expire=3600):
        '''
        Constructor
        user: the user name
        password: the password
        api_url: the url of the api
        page_size: the size of the page to use for pagination
        rate: the rate of requests per duration (default 2 requests per 1 seconds)
        duration: the duration in seconds of the rate limit (default 1 seconds)
        cache_expire: the duration in seconds to expire the cache (default 3600 seconds)

        Note: In a pod the cache is removed when the pod is killed or restarted
        '''
        self.user = user
        self.password = password
        self.api_url = api_url
        self.token = None
        self.headers = {
            'Content-Type': 'application/json',
        }
        # Set a controlled rate limit to prevent hitting the rate limit
        self.session = CachedLimiterSession(
            limiter=Limiter(RequestRate(rate, Duration.SECOND*duration)),
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache("primero.cache", expire_after=cache_expire)
        )
        self.page_size = page_size

        self.non_pii_cols = NON_PII_COLS

    def version(self):
        ''' Returns the version of the API library'''
        return get_version()

    def set_non_pii_cols(self, col_names=[]):
        """ Sets the whitelist of NON personal identifiable information columns

        These columns are not removed from the response of the server on methods that support anonymized data. 
        This does not apply to methods with the `_raw` postfix as these return directly the response from the server.

        Args:
            col_names (list, optional): columns names that hold PII that need to be removed. Defaults to [].
        """
        self.non_pii_cols = col_names
    
    def _anonymize_list(self, list_with_pii, additional_data:List = None):
        """
        Anonymizes a list of dictionaries by removing personally identifiable information (PII).
        Args:
            list_with_pii (list): A list of dictionaries containing PII.
            additional_data (List, optional): A list of additional non-PII columns to retain in the anonymized dictionaries. Defaults to None.
        Returns:
            list: A list of dictionaries with PII removed.
        """
        anonymized_list = []
        for dict_item in list_with_pii:
            # remove pii cols
            anonymized_item = self._extract_non_pii(dict_item, 
                                            additional_data=additional_data)
            anonymized_list.append(anonymized_item)
        return anonymized_list

    def _is_last_page(self, metadata):
        '''
        for a multi-page response, check if the current page is the last page
        metadata is the metadata object from the response which contains the 
        page, total and per parameters.
        '''

        page = metadata['page']  # current page
        total = metadata['total']  # total number of items
        per = metadata['per']  # number of items per page
        logger.debug('metadata=%s result=%s', metadata, (page * per) >= total)
        return (page * per) >= total

    def _call_api_get(self, url):
        '''
        calls the server API adding the (Basic) authentication
        '''
        response = self.session.get(
            url, headers=self.headers, auth=HTTPBasicAuth(self.user, self.password))
        if response.status_code != 200:
            logger.error('error calling primero server: %s: %s, url: %s',
                         response.status_code, response.text, url)
            return None
        # Convert to dict
        json = response.json()
        # check if data is part of json
        if 'data' not in json:
            return None
        return json['data']

    def _call_paginated_api(self, url: str):
        '''
        Calls the api with the given url and page_size.

        URL should not have per and page parameters
        Returns a list of data

        '''

        logger.debug('_call_paginated_api url=%s self.page_size=%s',
                     url, self.page_size)
        page_size = self.page_size
        page = 1
        data = []
        while True:
            get_url = url
            # Check if ? is present, add it if not
            if '?' not in get_url:
                get_url += '?'
            # Add &per=page_size&page=page to the url.
            get_url += f'&per={page_size}&page={page}'
            logger.debug('get_url: %s', get_url)
            response = self.session.get(
                get_url, headers=self.headers, auth=HTTPBasicAuth(self.user, self.password))
            # check if response is successful
            if response.status_code != 200:
                logger.error(
                    'Failed to get paginated data ${response.status_code}: ${response.text}, url: ${get_url}')
                continue

            # The response is a JSON object that contains the data and metadata objects.
            # data is an array of objects that contain the actual data
            # metadata contains information about the pagination

            # Extract the data from the response
            json_data = response.json()
            # extend the existing list to include new data
            data.extend(json_data['data'])
            # check if we are at the last page
            logger.debug('page=%s metadata=%s', page, json_data["metadata"])
            if self._is_last_page(json_data['metadata']):
                break
            page += 1
        return data

    def _extract_non_pii(self, data_dict, additional_data: List = None):
        """
        Removes personally identifiable information (PII) from a dictionary by keeping only self.non_pii_cols.

        You can set the non_pii_cols by using `self.et_non_pii_cols(["col", "col2", "col3"])`
        Args:
            data_dict (dict): The dictionary from which PII should be removed.
            custom_non_pii_cols (list, optional): Custom list of PII columns to remove. Defaults to None.
            additional_cols (list, optional): Additional columns to remove. Defaults to [].

        Returns:
            dict: The dictionary with PII and additional columns removed.
        """
        non_pii_cols = self.non_pii_cols.copy()
        if additional_data:
            non_pii_cols.extend(additional_data)
        
        for key in list(data_dict.keys()):
            if key not in non_pii_cols:
                del data_dict[key]
        return data_dict

    def get_cases_raw(self):
        """
        Fetches raw case data from the Primero API.

        This method constructs the URL for the 'cases' endpoint of the Primero API
        and makes a paginated API call to retrieve the raw case data.

        Returns:
        list: A list of raw case data retrieved from the API.
        """
        url = self.api_url + 'cases'
        return self._call_paginated_api(url)

    def get_cases(self, anonymized=True, additional_data:List=None):
        """
        Fetches case data from the Primero API.
        anonymized: if True, removes personally identifiable information (PII) from the case data before returning it. 
        additional_data: Additional columns to whitelist from the case data. This is useful if you need any column that is not whitelisted by default.`

        See the property `self.non_pii_cols` for the default list of non-PII columns.

        additional_non_pii_cons: Additional columns to whitelist from the case API response
        
        Returns:
        List A list of case data retrieved from the API.
        """
        cases = self.get_cases_raw()
        if anonymized:
            anonymized_cases = self._anonymize_list(cases, additional_data=additional_data)
            return pd.DataFrame(anonymized_cases)
        # otherwise return the raw data
        return pd.DataFrame(cases)

    def get_incidents_raw(self):
        """
        Fetches the list of incidents as they're returned by the API.  

        Returns:
            DataFrame: list of incidents fetched from the API
        """
        url = self.api_url + 'incidents'
        return self._call_paginated_api(url)

    def get_incidents(self, anonymized = True, additional_data:List=None):
        """
        Retrieve incidents data, by default anonymized.
        Parameters:
        -----------
        anonymized : bool, optional
            If True, the incidents data will be anonymized. Default is True.
        additional_data : List, optional
            A list of additional non-PII (Personally Identifiable Information) columns to include in the anonymized data. Default is None.
        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame containing the incidents data. If `anonymized` is True, the data will be anonymized.
        """
    
        incidents = self.get_incidents_raw()
        if anonymized:
            anonymized_incidents = self._anonymize_list(incidents, additional_data=additional_data)
            return pd.DataFrame(anonymized_incidents)
        return pd.DataFrame(incidents)
        
    def get_report_raw(self, report_id: int):
        """
        Gets the report with the given a report id
        returns a dictionary with the content of the report or None if there is an error.
        """

        url = self.api_url + 'reports/' + str(report_id)
        logger.debug('report_id: %s, get_report url=%s', report_id, url)
        return self._call_api_get(url)

    def get_report_list(self):
        """
        Returns a list of reports.
        The content of each report is a dictionary with some metadata.
        """
        url = self.api_url + 'reports'
        return self._call_paginated_api(url)

    def get_reports_raw(self):
        """"
        Gets the list of reports for the given.

        Returns a dictionary with the id as key and the report in Dict format as value
        The content of the report is a dictionary

        If while fetching the report there is an error (f.i no data), the content of that id is None.
        For example if there is an error in report 10, then 
        ```
            reports = primero.get_report_raw()
            reports[10]== None # True
        ```
   
        """
        reports = {}
        report_list= self.get_report_list()
        for report in report_list:
            report_id = report['id']
            logger.debug(f'getting report {report_id}')
            report = self.get_report_raw(report_id)
            # report is None if there is an error, we remove it from the list of reports.
            if report:
                reports[report_id] = report
        return reports

    def get_report(self, report_id: int, lang='en'):
        """"
        Gets the report with the given id
        returns a object of the Report class or None if there is an error.
        """
        logger.debug(f'get_report id={report_id}, lang={lang}')
        report_json_dict = self.get_report_raw(report_id)
        if report_json_dict is None:
            logger.error(f'Did not get report {report_id}')
            return None
        return Report(report_json_dict, lang)

    def get_reports(self, lang='en'):
        '''
        Gets the list of reports for the given page and page_size. 
        Returns a dictionary of Report objects with the id as key and the report as value
        '''
        reports = {}
        report_list = self.get_report_list()
        for report in report_list:
            id = report['id']
            report = self.get_report(id, lang)
            if report:
                reports[id] = report
        return reports

    def get_lookups(self):
        '''lookups are mapping between ids and human labels for the data'''
        url = self.api_url + 'lookups'
        return self._call_paginated_api(url)

    def get_server_version(self):
        url = self.api_url + 'contact_information'
        contact_information = self._call_api_get(url)
        logger.debug('contact_information_full_response: %s', contact_information)
        return contact_information['system_version']
