import bz2
import json
from tqdm import tqdm
import os


import warnings; warnings.simplefilter('ignore')
import random
import numpy as np
import pandas as pd

seed = 42
random.seed(seed)
np.random.seed(seed)

#NLP libraries
import spacy
from gensim.models.phrases import Phrases
from gensim.corpora import Dictionary
from gensim.models import LdaModel


from src.CONSTS import KEYWORDS_JSON_FILE_PATH

nlp = spacy.load("en_core_web_sm")
nlp.remove_pipe('parser')
nlp.remove_pipe('tagger')


STOPWORDS = spacy.lang.en.stop_words.STOP_WORDS

def process_quotes(quotes) -> list:
  """This function processes all quotes given in lines.
  Stopwords, punctuation and numbers are removed and entities added.
  param: lines: list
  return: processed_docs: list"""
  
  processed_quotes = list()

  for i, doc in tqdm(enumerate(nlp.pipe(quotes, batch_size=20))):   #TODO: batchsize different for different files
  
      # Process document using Spacy NLP pipeline.
      ents = doc.ents  # Named entities
  
      # Keep only words (no numbers, no punctuation).
      # Lemmatize tokens, remove punctuation and remove stopwords.
      doc = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
  
      # Remove common words from a stopword list and keep only words of length 3 or more.
      doc = [token for token in doc if token not in STOPWORDS and len(token) > 2]
  
      # Add named entities, but only if they are a compound of more than word.
      doc.extend([str(entity) for entity in ents if len(entity) > 1])
  
      processed_quotes.append(doc)
  
  processed_quotes = add_bigrams(processed_quotes)
  
  return processed_quotes


def add_bigrams(processed_quotes):
  """This function adds bigrams, which exist at least 15 times in all quotes,
  to the processed quotes
  param: processed_lines: list
  return: processed_lines: list"""
  
  bigram = Phrases(processed_quotes, min_count=15)
  for idx in range(len(processed_quotes)):
    for token in bigram[processed_quotes[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            processed_quotes[idx].append(token)
            
  return processed_quotes

def create_bag_of_words(processed_lines):
  """This function creates a bag of words representation for the quotes
  param: processed_lines: list
  return: dictionary: , corpus:"""
  
  
  # Create a dictionary representation of the documents, and filter out frequent and rare words.
  dictionary = Dictionary(processed_lines)
  
  # Remove rare and common tokens.
  # Filter out words that occur too frequently or too rarely.
  max_freq = 0.5
  min_wordcount = 5
  dictionary.filter_extremes(no_below=min_wordcount, no_above=max_freq)
  
  # Bag-of-words representation of the documents.
  corpus = [dictionary.doc2bow(quote) for quote in processed_lines]
  
  return dictionary, corpus

def assign_to_cluster(corpus, model):
  """This function assigns each quote to the found clusters of model"""

  sent_to_cluster = list()
  for n,doc in enumerate(corpus):
      if doc:
        cluster = max(model[doc],key=lambda x:x[1])
        sent_to_cluster.append(cluster[0])
        
  return np.array(sent_to_cluster)

def select_correct_topics(model, keywords):
  """This function selects which of the found clusters are of interest based on the keyword"""
  
  topic_numbers = list()

  all_words = list()
  for words in keywords:
    for word in words.split(" "):
      all_words.append(word)
  all_words = list(set(all_words))
  count = 0
  print(model.show_topics(num_words=5))
  for topic in model.show_topics(num_words=5):
    for word in all_words:
      if word in topic[1]:
        count += 1
    if count > 0:
      topic_numbers.append(topic[0])
      
  
  return topic_numbers


def filter_found_quotes_with_clustering(path, filter_list, n_topics):
  """This functions updates the files in a given folder defined by path. Only the 
  files in filter list are updated. The quotes in these folders are updated by
  applying a clustering model (LDA) on the quotes with five clusters. Any of the
  five found clusters which have one of the keywords of the topic are considered
  to be truly of the topic. At the end the quote files are updated.
  
  param:  path: str
          filter_list: list
          n_topics: int"""
          
  # load dictionary of the keywords
  with open(KEYWORDS_JSON_FILE_PATH, "r") as file:
    keywords = json.load(file)
  
  for filename in os.listdir(path):    # loop through all the files in a folder
    
    key = filename.split('-')[0].split('/')[-1].replace("_"," ")
    
    if key in filter_list:  # Only files of filter_list
      
      filename = path + filename
      
      with bz2.open(filename, "rt") as bzinput:
        df = pd.read_json(bzinput, compression = 'bz2', lines=True)
      
      # Process into bag of words
      dictionary, corpus = create_bag_of_words(process_quotes(df["quotation"]))
      
      # Train a model
      print("training ...")
      params = {'passes': 10, 'random_state': seed}
      base_models = dict()
      model = LdaModel(corpus=corpus, id2word=dictionary, num_topics = n_topics,
                      passes=params['passes'], random_state=params['random_state'])
      
      print("assigning ...")
      # assignment
      sent_to_cluster = assign_to_cluster(corpus, model)
      
      # Find which topics must be selected based on intial key words
      
      topic_numbers = select_correct_topics(model, keywords[key])
      
      # Find which quotes to keep
      lines_to_keep = np.zeros(len(sent_to_cluster), dtype=bool)
      for number in topic_numbers:
        lines_to_keep = np.logical_or(lines_to_keep, sent_to_cluster == number)
      
      # update Dataframe  
      df = df[:len(sent_to_cluster)]
      df = df.loc[lines_to_keep]
      
      # Show some output
      
      print(topic_numbers)
      for number in topic_numbers:
        sample = df["quotation"].sample(5)
        for line in sample:
          print(line)
        print('\n')
      
      break
# =============================================================================
#       print("saving ...")
#       # Update file
#       with open("test.json", 'w+') as bzoutput:
#         df.to_json(bzoutput)
#       
# =============================================================================
  return df
 

df = filter_found_quotes_with_clustering("generated/2015/",
                                    ["road injuries"], n_topics = 8)


    