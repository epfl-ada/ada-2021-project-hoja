"""
File name: synonym_utils.py
Author: HOJA
Date created: 4/12/2021
Date last modified: 4/12/2021
Python Version: 3.8
"""

import json
from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json
import pywikibot
import requests
from nltk.corpus import wordnet as wn
import time

import nltk
nltk.download('wordnet')


"""Functions of increasing number of keywords"""

# Main function

def add_new_synonyms(input_filename, output_filename):

    """
    This function extends the keywords given in the txt file of filename.
    The output is saved as a json file under the same name as filename.
    :param words: str
    """

    keywords = read_keywords(input_filename)

    start = time.time()
    for key in keywords.keys():
        print(key)
        baseline_keywords = keywords[key]
        old_n = len(baseline_keywords)
        
        keywords[key] = extend_with_wikidata(baseline_keywords)
        
        keywords[key] = extend_with_wordnet(keywords[key])
        keywords[key] = list(set(keywords[key]))
        
        print("time taken:", time.time() - start)
        print("total keywords:", len(keywords[key]))
        print("words added:", len(keywords[key]) - old_n)
        start = time.time()

        with open(output_filename, 'w+') as fp:
            json.dump(keywords, fp)
            
    print(output_filename)

"""Functions for wikidata aliases"""

def extend_with_wikidata(keywords):
  
  aliases = get_aliases_wikidata(keywords)
  
  # Remove useless aliases
  aliases = checknew_words(aliases, keywords)
  
  if aliases:
      keywords.extend(aliases)
      
  return keywords


def get_identifier(item) -> str:
    """This function finds the wikidata identifier for a given string input (item)
    input:
        -item: str, item of which you want the wikidata identfier
    output:
        : str, wikidata identfier"""

    params = dict(
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

    alias = list()

    for word in words:
        identifier = get_identifier(word)
        if identifier:
            site = pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            item = pywikibot.ItemPage(repo, identifier)

            if not item.isRedirectPage():
                if "en" in item.aliases:
                    alias.extend(item.aliases["en"])
    
    alias = [ali.lower() for ali in alias]
    return alias


""""Functions for synsets"""

def extend_with_wordnet(keywords):
  
  # replace space by _, works better for wordnet
  for i in range(len(keywords)):
    keywords[i] = keywords[i].replace(" ", "_")
    
  synonyms = get_all_synonyms(keywords)
  
  # reverse change
  for i in range(len(synonyms)):
    synonyms[i] = synonyms[i].replace("_", " ")
  
  for i in range(len(keywords)):
    keywords[i] = keywords[i].replace("_", " ")
    
  # Remove redundant synonyms
  synonyms = checknew_words(synonyms, keywords)
  
  if synonyms:
      keywords.extend(synonyms)
  
  return keywords


def get_all_synonyms(words) -> list:
    """
    Gets all related words to the input words via the wordnet databank.
    
    Relations are hyponyms and derivationally derived words.
    The first synset is taken to be the the correct synset to use.
    :param words: list
    :return output_words: list
    """

    output_words = []
    synsets = get_synsets_input_words(words, word_type = 'n')
    
    if synsets:
      synset_words = synsets
      
      """To get everything, potentially lots of unrelated words, change the line above to:
        synset_words = synsets""" 
  
      lemma_words = []
      output_lemmas = []

      while len(synset_words) > 0 or len(lemma_words) > 0:
          # for i in range(20):
          if len(synset_words) > 0:

              # take first word on the list for new search
              current_search = synset_words[0]
              synset_words, lemma_words, output_lemmas = update_synsets(current_search, synset_words, lemma_words, output_lemmas)
          if len(lemma_words) > 0:
              # take first word on the list for new search
              current_search = lemma_words[0]
              
              output_words, lemma_words, output_lemmas = update_lemmas(current_search, output_words, lemma_words, output_lemmas)
              
              

    return output_words
  
  

def get_synsets_input_words(words, word_type) -> list:
    """
    Gets all synsets for a list of words. Returns only synsets of given word type
    :param words: list, word_type: str
    :return synsets: list
    """
    synsets = []
    for word in words:
      word_synsets = wn.synsets(word)
      
      # Hard coded these exeptions if more are found, they should be added here.
      if word == 'stroke':
        synsets.append(wn.synset('stroke.n.03'))
      elif word == 'aids':
        synsets.append(wn.synset('AIDS.n.01'))
      
      
      else:
        for synset in word_synsets:
          if synset.pos() == word_type and synset.lemmas()[0].name() == word:
            synsets.append(synset)
          
    return synsets

def update_synsets(synset, synset_words, lemma_words, output_lemmas):
  
  # remove word from search list
  synset_words.remove(synset)
  new_synsets = synset.hyponyms()
  for new in new_synsets:
    if new.pos() == 'n':
      synset_words.append(new)
    
  new_found = list()
  new_found.extend(synset.lemmas())
  for item in new_found:
      if item not in output_lemmas and item.synset().pos() == 'n':
          lemma_words.append(item)
  
  return synset_words, lemma_words, output_lemmas



def update_lemmas(lemma, output_words, lemma_words, output_lemmas):
  # Add the word to output list
  lemma_name_no_underscore_lowercase = lemma.name().replace("_", " ").lower()
  output_words.append(lemma_name_no_underscore_lowercase)
  output_lemmas.append(lemma)
  # remove word from search list
  lemma_words.remove(lemma)
              
  new_found = list()
  new_found.extend(lemma.derivationally_related_forms())
  #TODO: remove this/only for input keyword? ~500 words difference (3500->3000)

  for item in new_found:
      if item not in output_lemmas and item.synset().pos() == 'n':
          lemma_words.append(item)
          
  return output_words, lemma_words, output_lemmas
   
                   
"""General utility functions"""


def checknew_words(new_words, old_words):
  """Remove sub set words. E.g. if keywords contains meningitis and 
  aliases spinal meningitis, remove spinal meningitis.
  Also removes words shorter than len 3."""
  
  new_words = [word for word in new_words if len(word) > 3 and '.' not in word]
  
  # remove redundant words  
  words_to_check = new_words
  new_words = list()
  while words_to_check:
    check = words_to_check[0]
    del words_to_check[0]
    
    useless = 0
    for old_word in old_words:
      if len(old_word.split(' ')) == 1:
        for word in check.split(' '):
          if word == old_word:
            useless = 1
            break
        
      if len(old_word.split(' ')) > 1 and old_word in check:
        useless = 1
        
      if useless:
        break
      
    if not useless:
      new_words.append(check)
  
  
  return new_words            



def read_keywords(filename) -> dict():
    keywords = dict()

    with open(filename, "r") as file: 
        for line in file:
            line = line.lower()
            line = line.replace("\n", "")
            line = line.split('<>')
            keywords[line[0]] = line

    return keywords



