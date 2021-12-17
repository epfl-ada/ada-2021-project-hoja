"""
File name: add_features.py
Author: HOJA
Date created: 03/12/2021
Date last modified: 17/12/2021
Python Version: 3.8
"""

import json
import pywikibot
import collections
import numpy as np
from src.CONSTS import COUNTRY_IDENTIFIER, SPEAKER_ATTRIBUTES, URL_END_LIB, URL_COUNTRY
import requests
import time


"""FUnctions to get country of speaker"""

def get_country_from_wikidata(q_country) -> str:
    """This function finds the country of a q-identifier on wikidata.
    param:  q_country: str
    return: : str
    """
    country = None
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    try:
        item = pywikibot.ItemPage(repo, q_country)
    except ConnectionError:
        return country
      
    item_dict = item.get()
    try: 
        country = item_dict['labels']['en']
    except KeyError:
        pass
      
    return country
      


def get_country_identifier(q_person) -> list:
    """
    This functions returns the country identifier of a given person identifier
    param: q_person: list
    return: q_country: list
    """    
    q_country = list()
    for identfier in q_person:
        if identfier in SPEAKER_ATTRIBUTES:
            q_identifiers = SPEAKER_ATTRIBUTES[identfier].tolist()
            
            if q_identifiers:
              for q in q_identifiers:
                  if isinstance(q, (list, np.ndarray)):
                      q_country.append(q[0])
                  elif q:
                      q_country.append(q)
        
    return q_country

def get_most_common_values_list(input_list) ->list:
    """
    This function returns a list of most common values in input list.
    param: input_list: list
    return: output_list: list
    """
    output_list =list()
    freq_map = collections.Counter(input_list)
    max_freq = freq_map.most_common(1)[0][1]
    for key in freq_map.keys():
        if freq_map[key] == max_freq:
            output_list.append(key)      
    return output_list

     
def assign_country_to_speaker(q_person) ->list:
    """ This function finds the country(ies) of a list of qids of a person.
    param: q_person: list
    return: speaker_country: list
    """
    q_country = get_country_identifier(q_person)
    # Get most common country if multiple found
    if q_country:
        q_country = get_most_common_values_list(q_country)
    
    # Multiple countries found for speaker    
    if len(q_country) > 1:
        speaker_country = list()
        for id_country in q_country:
            if id_country in COUNTRY_IDENTIFIER:
                speaker_country.append(COUNTRY_IDENTIFIER[id_country])
            else:
                country = get_country_from_wikidata(id_country)
                speaker_country.append(country)
                COUNTRY_IDENTIFIER[id_country] = country
     
    # One country found           
    elif len(q_country) == 1:
        id_country = q_country[0]
        if id_country in COUNTRY_IDENTIFIER:
            speaker_country = COUNTRY_IDENTIFIER[id_country]
        else:
            country = get_country_from_wikidata(id_country)
            speaker_country = country
            COUNTRY_IDENTIFIER[id_country] = country
        
    # No country found
    else:
      speaker_country = None
    return speaker_country


"""Functions to get country of url"""

def get_identifier(item) -> str:
    """This function finds the wikidata identifier for a given string input (item)
    input:
        -item: str, item of which you want the wikidata identfier
    output:
        : str, wikidata identfier"""
    
    params = dict (
            action='wbsearchentities',
            format='json',
            language='en',
            uselang='en',
            type='item',
            search=item
            )
    
    response = None
    try:
        response = requests.get('https://www.wikidata.org/w/api.php?', params).json()
    except ValueError or ConnectionError:
        pass
    
    if response:
        if response.get('search'):
            return response.get('search')[0]['id']

def get_country_from_identifier(q_website):
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    try:
      item = pywikibot.ItemPage(repo, q_website)
    except ConnectionError:
      return None
    
    country = None
    if not item.isRedirectPage():
        item_dict = item.get()
        if "P17" in item_dict["claims"]:
            clm_list = item_dict["claims"]["P17"]
            for clm in clm_list:
                clm_trgt = clm.getTarget()   
                if clm_trgt:
                    try:
                        country = clm_trgt.text["labels"]["en"]
                    except KeyError:
                        pass
                    return country
      
def get_country_website(url) -> str:  
    """This function finds the country in which the company of the url is based,
    e.g. for www.guardian.co.uk it will return Great-Brittain
    input:
        url: str, url of which the country needs to be found
        url_end_dic: dict, dictionary of countries for which url was already found
    output:
        country: str, found country"""
    
    country =  None

    url_ending = url.split('.')[-1]
    if url_ending in URL_END_LIB:
        country = URL_END_LIB[url_ending]
    
    """ Change this back before Final push
    else:
        q_website = get_identifier(url)
        if q_website:
            country = get_country_from_identifier(q_website)

        if q_website is None or country is None:
            url_try_list = url.split('.')
            url_try = max(url_try_list, key=len)
            q_website = get_identifier(url_try)
            if q_website:
                country = get_country_from_identifier(q_website)
    """      
    return country

def assign_country_to_url(urls) -> list:
    """This function finds all the countries of the url list
    param: urls: list
    return: countries: list"""
    
    countries = list()
    for url in urls:
        if url in URL_COUNTRY:
            countries.append(URL_COUNTRY[url])
        else:
            country = get_country_website(url)
            URL_COUNTRY[url] = country
            countries.append(country)
      
    return countries

def expand_line(line):
    """Adds the country of the speaker, urls and unique urls to the line
    param: line: json
    return: expanded_line: json"""
    # load from json
    parsed = json.loads(line)
    
    # adapt for country speaker
    q_person = parsed['qids']
    if q_person:
        speaker_country = assign_country_to_speaker(q_person)
    else:
        speaker_country = [] 
    parsed['country_speaker'] = speaker_country
    
    # adapt for country url
    urls = parsed['urls']
    unique_urls = list()
    for url in urls:
        new_url = url.split('/')[2]
        new_url = new_url.split('?')[0]
        new_url = new_url.split(':')[0]
        unique_urls.append(new_url)

    unique_urls = list(set(unique_urls)) 
    parsed['n_appearances'] = len(unique_urls)
    url_countries = assign_country_to_url(unique_urls)
    parsed['country_urls'] = url_countries
    
    # back to json
    expanded_line = json.dumps(parsed).encode('utf-8')
    return expanded_line




