# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 14:44:51 2021

@author: jurri
"""

import json
import pywikibot
import collections
import numpy as np
from src.CONSTS import COUNTRY_IDENTIFIER, SPEAKER_ATTRIBUTES


def get_country_from_wikidata(q_country) -> str:
    """This function finds the country of a q-identifier on wikidata.
    param:  q_country: str
    return: : str
    """
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()
    item = pywikibot.ItemPage(repo, q_country)
    item_dict = item.get()
    if item_dict['labels']['en']:
        return item_dict['labels']['en']
      


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
  

def expand_line(line):
    """Adds the country of the speaker to the line
    param: line: json
    return: expanded_line: json"""
    # load from json
    parsed = json.loads(line)
    # adapt
    q_person = parsed['qids']
    if q_person:
        speaker_country = assign_country_to_speaker(q_person)
    else:
        speaker_country = []
     
    parsed['country_speaker'] = speaker_country
    # back to json
    expanded_line = json.dumps(parsed).encode('utf-8')

    return expanded_line













