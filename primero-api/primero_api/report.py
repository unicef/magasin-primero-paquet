
from .report_processors import process_report, report_name, report_slug, get_report_labels, report_description
from .logger import logger

class Report:
    def __init__(self, report_data_dict, lang='en'):
        '''
        report_data_dict is the dictionary that comes from the API
        lang is the language to use for the report
        '''
        if 'id' not in report_data_dict:
            logger.error(f'Report does not have an id: {report_data_dict}')
            return None
        if report_data_dict is None:
            logger.error(f'Report is None')
            return None
        id = report_data_dict['id']
        #logger.debug(f'report data: {report_data_dict}')
        logger.debug(f'Creating Report object for {id}, lang={lang}')

        self.report_data_dict = report_data_dict
        self.id = report_data_dict['id']
        self.lang = lang
        
        self.slug = report_slug(report_data_dict, lang)
        self.name = report_name(report_data_dict, lang)
        self.description = report_description(report_data_dict, lang)
        
    def __str__(self):
        return f'Report {self.id} ({self.name})'    
    
    
    def to_pandas(self):
        return process_report(self.report_data_dict, lang=self.lang)
    
    def labels(self):
        return get_report_labels(self.report_data_dict, lang=self.lang)
    
    
