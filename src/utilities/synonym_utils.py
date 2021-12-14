"""
File name: synonym_utils.py
Author: HOJA
Date created: 4/12/2021
Date last modified: 11/12/2021
Python Version: 3.8
"""

import json
import pywikibot
import requests
from nltk.corpus import wordnet as wn
from src.CONSTS import KEYWORDS_FILE_PATH, KEYWORDS_JSON_FILE_PATH, KEYWORD_STOPWORDS, KEYWORD_DIABETES_TYPE2, KEYWORD_TERRORISM_WAR

import nltk

nltk.download('wordnet')

"""Functions of increasing number of keywords"""


def add_new_synonyms():
    """
    This function extends the keywords given in the txt file of filename.
    The output is saved as a json file under the same name as filename.
    """

    keywords = read_keywords(KEYWORDS_FILE_PATH)

    print("Adding New Synonyms...")

    for key in keywords.keys():

        if key == KEYWORD_DIABETES_TYPE2:
            continue

        baseline_keywords = keywords[key]

        keywords[key] = extend_with_wikidata(baseline_keywords)
        keywords[key] = list(set(keywords[key]))
        keywords[key] = extend_with_wordnet(keywords[key])
        keywords[key] = list(set(keywords[key]))
        if key == KEYWORD_TERRORISM_WAR:
            keywords[key].remove('the base')
        remove_any_stopword_keyword(keywords[key])

        with open(KEYWORDS_JSON_FILE_PATH, 'w+') as fp:
            json.dump(keywords, fp)


def remove_any_stopword_keyword(keyword):
    for stopword in KEYWORD_STOPWORDS:
        if stopword in keyword:
            keyword.remove(stopword)


"""Functions for wikidata aliases"""


def extend_with_wikidata(keywords):
    """
    This functions extends keywords list by finding aliases
  on wikidata for keywords
  param: keywords: list
  return: keywords: list
  """

    aliases = get_aliases_wikidata(keywords)

    if aliases:
        keywords.extend(aliases)

    # Remove redundant synonyms
    keywords = checknew_words(keywords)

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
        if word != 'war':
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


def extend_with_wordnet(keywords) -> list:
    """This fucntions extends keywords list by finding hyponyms and lemmas
  in the wordnet database for keywords
  param: keywords: list
  return: keywords: list"""

    # replace space by _, works better for wordnet
    for i in range(len(keywords)):
        keywords[i] = keywords[i].replace(" ", "_")

    synonyms = get_all_synonyms(keywords)

    # reverse change
    for i in range(len(synonyms)):
        synonyms[i] = synonyms[i].replace("_", " ")

    for i in range(len(keywords)):
        keywords[i] = keywords[i].replace("_", " ")

    if synonyms:
        keywords.extend(synonyms)

    # Remove redundant synonyms
    keywords = checknew_words(keywords)

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
    synsets = get_synsets_input_words(words, word_type='n')

    if synsets:
        synset_words = synsets

        lemma_words = []
        output_lemmas = []

        while len(synset_words) > 0 or len(lemma_words) > 0:
            # for i in range(20):
            if len(synset_words) > 0:
                # take first word on the list for new search
                current_search = synset_words[0]
                synset_words, lemma_words, output_lemmas = update_synsets(current_search, synset_words, lemma_words,
                                                                          output_lemmas)
            if len(lemma_words) > 0:
                # take first word on the list for new search
                current_search = lemma_words[0]

                output_words, lemma_words, output_lemmas = update_lemmas(current_search, output_words, lemma_words,
                                                                         output_lemmas)

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
        elif word == 'fire':
            synsets.append(wn.synset('fire.n.01'))
        elif word == 'consumption':
            synsets.append(wn.synset('pulmonary_tuberculosis.n.01'))

        else:
            for synset in word_synsets:
                if synset.pos() == word_type and synset.lemmas()[0].name() == word:
                    synsets.append(synset)

    return synsets


def update_synsets(synset, synset_words, lemma_words, output_lemmas):
    """Finds new synsets based on the hyponyms of synset. synset_words, lemmas_words
  and output_lemmas are updated accordingly
  param:  synset: nltk.corpus.reader.wordnet.Synset
          synsets_words: list
          lemma_words: list
          output_lemmas: list
          
  return: synsets_words: list
          lemma_words: list
          output_lemmas: list"""

    # remove word from search list
    synset_words.remove(synset)
    new_synsets = synset.hyponyms()
    for new in new_synsets:
        if new.pos() == 'n':
            synset_words.append(new)

    new_found = list()
    new_found.extend(synset.lemmas())
    for item in new_found:
        if item not in output_lemmas and item.synset().pos() == 'n' and len(item.name()) > 2:
            lemma_words.append(item)

    return synset_words, lemma_words, output_lemmas


def update_lemmas(lemma, output_words, lemma_words, output_lemmas):
    """Adds lemma name to the outut words and updates the other lists.
  param:  synset: nltk.corpus.reader.wordnet.Lemma
          synsets_words: list
          lemma_words: list
          output_lemmas: list
          
  return: synsets_words: list
          lemma_words: list
          output_lemmas: list"""

    # Add the word to output list
    lemma_name_no_underscore_lowercase = lemma.name().replace("_", " ").lower()
    output_words.append(lemma_name_no_underscore_lowercase)
    output_lemmas.append(lemma)
    # remove word from search list
    lemma_words.remove(lemma)

    return output_words, lemma_words, output_lemmas


"""General utility functions"""


def checknew_words(old_words):
    """Remove sub set words. E.g. if keywords contains meningitis and
  aliases spinal meningitis, remove spinal meningitis.
  Also removes words shorter than len 3."""

    old_words = [word for word in old_words
                 if len(word) > 3
                 and ('.' or '(' or '/' or '{' or ',' or ';') not in word and
                 len(word.split(" ")) < 4]

    new_words = filter_keywords(old_words)

    return new_words


def filter_keywords(keywords):
    """"Filters out redundant keywords. E.g. if keywords contains meningitis and
  aliases spinal meningitis, remove spinal meningitis."""

    compare = keywords.copy()
    output = list()

    while compare:
        check = compare[0]
        del compare[0]
        useless = 0

        for word in keywords:
            if word != check:
                if len(check.split(' ')) > 1:
                    in_count = 0
                    for sub in word.split(' '):
                        if sub in check.split(' '):
                            in_count += 1

                    if in_count == len(word.split(' ')):
                        useless = 1
                        break

        if useless == 0:
            output.append(check)

    return output


def read_keywords(filename) -> dict():
    """Reads keywords in a text file into a dict.
  param: filename: str
  return: keywords: dict
  """

    keywords = dict()

    with open(filename, "r") as file:
        for line in file:
            line = line.lower()
            line = line.replace("\n", "")
            line = line.split('<>')
            keywords[line[0]] = line

    return keywords
