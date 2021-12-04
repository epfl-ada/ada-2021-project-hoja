"""
File name: quotebank_preprocessing_utils.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

import os
import json
from src.CONSTS import DATA_PATH, GENERATED_PATH
from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json
import pywikibot
import requests
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import time


#TODO: refactoring this


def compose_quotebank_filenames() -> list:
    """
    Compose all the quotebank filenames to be read
    :return: list
    """
    quotes_file_list = []
    for i in range(8, 18):
        year = create_year_string_from_number(i)
        quotes_file_list.append(DATA_PATH + "quotes-" + year + ".json.bz2")
    return quotes_file_list


def create_directories_for_every_year():
    """
    For each year, create the corresponding directory where all the output files of each keyword will be stored
    """
    for i in range(8, 18):
        year = create_year_string_from_number(i)
        path = GENERATED_PATH + year + "/"
        os.makedirs(path, exist_ok = True)


def format_filenames_nicely(filename) -> str:
    """
    Replace any occurrences of unwanted characters in filenames, according to a specific format
    :param filename: str
    :return: str
    """
    special_chars = "!#$%^&*()/ "
    for special_char in special_chars:
        filename = filename.replace(special_char, '_')

    filename_without_comma = filename.replace(",", "")
    return filename_without_comma


def create_year_string_from_number(number) -> str:
    """
    Helper function to return a specific year given a number (index)
    :param number: int
    :return: str
    """
    if number < 10:
        year = "200" + str(number)
    else:
        year = "20" + str(number)
    return year


def get_all_years() -> list:
    """
    Get a list all of the years, for the files to be read
    :return: list
    """
    years_for_file = []
    for i in range(8, 18):
        year = create_year_string_from_number(i)
        years_for_file.append(year)

    return years_for_file


def extract_quotation(line) -> str:
    """
    Return the quotation from a parsed json
    :param line: str
    :return: str
    """
    json_line = json.loads(line)
    return json_line['quotation']
  


def get_all_synonyms(words):
  """
  Gets all related words to the input words via the wordnet databank. Relations are hyponyms and derivationally derived words.
  The first synset is taken to be the the correct synset to use.
  :param words: list
  :return output_words: list
  """
  
  output_words = []
  
  synsets = []
  for word in words:
    synsets.extend(wn.synsets(word))
  
  if synsets:
    synset_words = [synsets[0]]
    
    lemma_words = []
    output_lemmas = []
    
    while len(synset_words) > 0 or len(lemma_words) > 0:
    #for i in range(20):
      
      if len(synset_words) > 0:
        
        # take first word on the list for new search
        current_search = synset_words[0]
        # remove word from search list
        synset_words.remove(current_search)
        
        synset_words.extend(current_search.hyponyms())
        #synset_words.extend(current_search.member_holonyms())
        
        new_found = list()
        new_found.extend(current_search.lemmas())
        for item in new_found:
          if item not in output_lemmas:
            lemma_words.append(item)
            
      if len(lemma_words) > 0:
        # take first word on the list for new search
        current_search = lemma_words[0]
        # Add the word to output list
        output_words.append(current_search.name().replace("_", " "))
        output_lemmas.append(current_search)
        # remove word from search list
        lemma_words.remove(current_search)
        
        new_found = list()
        new_found.extend(current_search.derivationally_related_forms())
    
        for item in new_found:
          if item not in output_lemmas:
            lemma_words.append(item)

  return output_words


"""Functions of increasing number of keywords"""

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

    response = requests.get('https://www.wikidata.org/w/api.php?', params).json()
    if response.get('search'):
        return response.get('search')[0]['id']
    
def get_aliases_wikidata(words) -> list:
  """
  Gets all aliases of a word via wikidata.
  :param words: list
  :return : list
  """
  
  aliases = list()
  
  for word in words:
    identifier = get_identifier(word)
    if identifier:
      site = pywikibot.Site("wikidata", "wikidata")
      repo = site.data_repository()
      item = pywikibot.ItemPage(repo, identifier)
        
      if not item.isRedirectPage():
        if "en" in item.aliases:
          aliases.extend(item.aliases["en"])
        
  return aliases
    
    
def get_all_synonyms(words) -> list:
  """
  Gets all related words to the input words via the wordnet databank. Relations are hyponyms and derivationally derived words.
  The first synset is taken to be the the correct synset to use.
  :param words: list
  :return output_words: list
  """
  
  output_words = []
  synsets = []
  for word in words:
    synsets.extend(wn.synsets(word))
  
  if synsets:
    synset_words = [synsets[0]]
    
    lemma_words = []
    output_lemmas = []
    
    while len(synset_words) > 0 or len(lemma_words) > 0:
    #for i in range(20):
      
      if len(synset_words) > 0:
        
        # take first word on the list for new search
        current_search = synset_words[0]
        # remove word from search list
        synset_words.remove(current_search)
        
        synset_words.extend(current_search.hyponyms())
        #synset_words.extend(current_search.member_holonyms())
        
        new_found = list()
        new_found.extend(current_search.lemmas())
        for item in new_found:
          if item not in output_lemmas:
            lemma_words.append(item)
            
      if len(lemma_words) > 0:
        # take first word on the list for new search
        current_search = lemma_words[0]
        # Add the word to output list
        output_words.append(current_search.name().replace("_", " "))
        output_lemmas.append(current_search)
        # remove word from search list
        lemma_words.remove(current_search)
        
        new_found = list()
        new_found.extend(current_search.derivationally_related_forms())
    
        for item in new_found:
          if item not in output_lemmas:
            lemma_words.append(item)

  return output_words   
 
def read_keywords(filename) -> dict():
  keywords = dict()
  
  with open(filename) as file:
    for line in file:
      line = line.replace("\n", "")
      line = line.split('<>')
      keywords[line[0]] = line
      
  return keywords 

  
def add_new_synonyms(filename):
  """
  This function extends the keywords given in the txt file of filename.
  The output is saved as a json file under the same name as filename.
  :param words: str
  """
  
  keywords = read_keywords(filename)

  start = time.time()
  for key in keywords.keys():
    print(key)
    aliases = get_aliases_wikidata(keywords[key])
    aliases = [word for word in aliases if len(word) > 3]
  
    if aliases:
      keywords[key].extend(aliases)
    
    keywords[key].extend(get_all_synonyms(keywords[key]))
    print("time taken:", time.time() - start)
    print("total keywords:", len(keywords[key]))
    start = time.time()
  
    keywords[key] = list(set(keywords[key]))
      
    with open(filename[:-3] + 'json', 'w') as fp:
      json.dump(keywords, fp)
      