import pandas as pd
from slugify import slugify

from .logger import logger

#
# Utility tools for processing reports
#

def report_description(report, lang='en'):
    '''
    Returns the name for the report in the given language.
    If the report does not have a name, it returns ''
    if the language is not in the name, it returns the english description
    if the english description is not available, it returns ''
    '''
    # check if report has a name
    if 'description' not in report:
        return ''
    # check if the language is in the name
    if lang not in report['description']:
        # check if english is in the name
        if 'en' not in report['description']:
            return ''
        lang = 'en'
    return report['description'][lang]

    

def report_name(report, lang='en'):
    '''
    Returns the name for the report in the given language.
    If the report does not have a name, it returns report-{report_id}
    if the language is not in the name, it returns the english name
    if the english name is not in the name, it returns report-{report_id}
    '''
    # check if report has a name
    if 'name' not in report:
        return 'report-' + report['id']
    # check if the language is in the name
    if lang not in report['name']:
        # check if english is in the name
        if 'en' not in report['name']:
            return 'report' + report['id']
        lang = 'en'
    return report['name'][lang]


def report_slug(report, lang='en'):
    '''
    Returns the slug for the report in the given language.
    If the report does not have a name, it returns report-{report_id}
    if the language is not in the name, it returns the english name
    if the english name is not in the name, it returns report-{report_id}
    '''
    name = report_name(report, lang)
    return slugify(name)


def find_key_in_dict(nested_dict, key):
    '''
    Find all values for a key in a nested dictionary
    returns a list of values
    '''
    found_items = []
    def search_dict(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == key:
                    found_items.append(v)
                if isinstance(v, dict):
                    search_dict(v)
                elif isinstance(v, list):
                    for item in v:
                        search_dict(item)
    search_dict(nested_dict)
    return found_items

def get_report_labels(report, lang='en'):
    '''
    Returns the labels for the report in the format (data contained in option_labels, in the original api response)
    Some reports may not contain labels, in that case it returns an empty dictionary

        label[id] = display_text
    '''
    all_labels=find_key_in_dict(report, 'option_labels')
    # returns this format
    #  
    #[ {en": [ 
    #     { "id": "sexually_exploited", "display_text": "Sexually Exploited"}, 
    #      ..., 
    #      {...} 
    #   ],
    #  fr: {...}
    #   ...
    #  {en": [ 
    #     { "id": "sexually_exploited", "display_text": "Sexually Exploited"}, 
    #      ..., 
    #      {...} 
    #   ],
    #  fr: {...}
    #   ... 
    # ]
    # we will convert to 
    #   label[id]= display_text
    #  example: 
    #   label[sexually_exploited] = "Sexually Exploited"
    labels = {}
    for labels_by_lang in all_labels:
        if lang in labels_by_lang:
            for label in labels_by_lang[lang]:
                labels[label['id']] = label['display_text']
    return labels    
    

def process_report(report, lang='en'):
    '''
    Process the report and return a dataframe

    report is the json object output of the api
    lang is the language to use for the labels

    '''
    
    if 'report_data' not in report:
        # return empty dataframe if there is no report data
        return pd.DataFrame()
    
    labels = get_report_labels(report, lang)
    # Example of report_data
    #
    #  report_data: {
    #   'sexually_exploited': {'_total': 0}, # it is just total
    #   'migrant': {
    #        '_total': 1,  # it contains total and desagregated data
    #        'male': {'_total': 1}, 
    #        'female': {'_total': 0}}, 
    #
    # Is converted to:
    #    key                    total  male female
    #    ---------------------  -----  ---- ------
    #    sexually_exploited     0
    #    migrant                1      1     0

    report_data = report['report_data']
    data = []
    #print('report_data', report_data)
    for key in report_data:
        datum = report_data[key].copy()
        #print("key", key, "datum:", datum)
        for k in datum.keys():
        # check if k is an object
        #print('k', k, type(datum[k])) 
            if type(datum[k]) is not int:
                datum[k] = datum[k]['_total']
        #print(key, datum)
        datum['key']= key

        # find the label for the key. default to key
        if key in labels:
            datum['key_label'] = labels[key]
        else:
            datum['key_label'] = key  

        # replace _total with total
        datum['total'] = datum['_total']
        datum.pop('_total')

        #print("added", datum)
        data.append(datum)
    
    # To data frame
    df = pd.DataFrame(data)
    return df
