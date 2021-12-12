# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 18:36:17 2021

@author: jurri
"""
# general
import bz2
import json
import os
from src.CONSTS import KEYWORDS_JSON_FILE_PATH, TOPICS_FOR_CLUSTERING
import time
import pandas as pd
from src.utilities import quotebank_preprocessing_utils as utils
 

# For clustering
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

"This function for the object of QuoteBankData"

def filter_quotes(json_lines, keywords, key):
    """The quotes are updated by vectorizing the quotes with SentenceTransformers
    and clustering with HDBSCAN.
    Clusters for which at least two of the ten most important words are in the keywords
    are kept.
    
    param:  json_lines: list
            keywords: list
            
    return: correct_quotes: list"""
    
    quotes = list()
    for line in json_lines:
      quotes.append(utils.extract_quotation(line))
    
    # cluster data
    cluster = cluster_quotes(quotes)
    
    # Keep the right clusters
    print("assigning ...")
    quotes_df = pd.DataFrame(quotes, columns=["quotation"])
    quotes_df['Topic'] = cluster.labels_
    quotes_per_topic = quotes_df.groupby(['Topic'], as_index = False).agg({'quotation': ' '.join})
    
    tf_idf, count = c_tf_idf(quotes_per_topic.quotation.values, m=len(quotes))
    # Get top 10 words per topic
    top_n_words = extract_top_n_words_per_topic(tf_idf, count, quotes_per_topic, n=10)
    # Get topics which have at least 2 words in their top 10 which are also in the keyword list
    if key == "poisonings":   # hard coded exception
        keywords.extend(["lead", "water", "food","arsenic"])
        
    correct_clusters = select_correct_topics(top_n_words, keywords)
    
    # Get indices of correct quotes
    lines_to_keep = np.zeros(len(quotes_df), dtype=bool)
    for cluster in correct_clusters:
      lines_to_keep = np.logical_or(lines_to_keep, quotes_df['Topic'] == cluster)
        
    json_lines = np.array(json_lines)[lines_to_keep].tolist
    
    return json_lines

"""The functions and the pipeline in this file have largely been implemented from:
  https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6
  """
  
  
def cluster_quotes(data):
  """Thsi functions clusters the quotes in data. SentenceTransformers from BERT is
  used to create embeddings. Better than LDA, since semantic differences are better
  distinguished. next the dimensionality is reduced with UMAP. Finally the quotes
  are clustered with a dbscan method (of HDBSCAN) so we do not need to determine
  the number of topics before hand"""
  
  start = time.time()
  print("Embedding...")
  model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
  embeddings = model.encode(data)
  print(time.time()-start)
  
  start = time.time()
  print("Reducing...")
  umap_embeddings = umap.UMAP(n_neighbors=15, 
                              n_components=10, 
                              metric='cosine').fit_transform(embeddings)
  print(time.time()-start)
  
  start = time.time()
  print("Clustering...")
  cluster = hdbscan.HDBSCAN(min_cluster_size=5,
                            metric='euclidean',                      
                            cluster_selection_method='eom').fit(umap_embeddings)
  print(time.time()-start)

  return cluster

def c_tf_idf(documents, m, ngram_range=(1, 1)):
    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count
  
def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=10):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    return top_n_words

  
def select_correct_topics(top_words, keywords) -> list:
  """This function selects which of the found clusters are of interest based on the keyword.
  param: top_words
          keywords: list
  returns:  topic_numbers: list"""
  
  topic_numbers = list()

  all_words = list()
  for words in keywords:
    for word in words.split(" "):
      all_words.append(word)
  all_words = list(set(all_words))
  
  
  for index in top_words:
    count = 0
    for word in all_words:
      if word in top_words[index]:
        
        count += 1
    if count > 1:
      topic_numbers.append(index)
      
  return topic_numbers


    
"This function is for separate use"

def filter_quotes_with_BERT(path, filter_list):
  """This functions updates the files in a given folder defined by path. Only the 
  files in filter list are updated. The quotes in these folders are updated by
  vectorizing the quotes with SentenceTransformers and clustering with HDBSCAN.
  Clusters for which at least two of the ten most important words are in the keywords
  are kept.
  
  param:  path: str
          filter_list: list"""
          
  # load dictionary of the keywords
  with open(KEYWORDS_JSON_FILE_PATH, "r") as file:
    keywords = json.load(file)
  
  for filename in os.listdir(path):    # loop through all the files in a folder
    
    key = filename.split('-')[0].split('/')[-1].replace("_"," ")
    if key in filter_list:  # Only files of filter_list
      
      filename = path + filename
      
      with bz2.open(filename, "rt") as bzinput:
        df = pd.read_json(bzinput, compression = 'bz2', lines=True)
        
      quotes = df["quotation"].to_list()
      
      # cluster data
      cluster = cluster_quotes(quotes)
      
      # Keep the right clusters
      print("assigning ...")
      quotes_df = pd.DataFrame(quotes, columns=["quotation"])
      quotes_df['Topic'] = cluster.labels_
      quotes_per_topic = quotes_df.groupby(['Topic'], as_index = False).agg({'quotation': ' '.join})
      
      tf_idf, count = c_tf_idf(quotes_per_topic.quotation.values, m=len(quotes))
      # Get top 10 words per topic
      top_n_words = extract_top_n_words_per_topic(tf_idf, count, quotes_per_topic, n=10)
      # Get topics which have at least 2 words in their top 10 which are also in the keyword list
      good_words = keywords[key] 
      if key == "poisonings":
          good_words.extend(["lead", "water", "food","arsenic"])
          
      correct_clusters = select_correct_topics(top_n_words, good_words)
      
      # Find which quotes to keep
      lines_to_keep = np.zeros(len(quotes_df), dtype=bool)
      for cluster in correct_clusters:
        lines_to_keep = np.logical_or(lines_to_keep, quotes_df['Topic'] == cluster)
        
    
      # update Dataframe  
      df = df.loc[lines_to_keep]
      
      print("saving ...")
      # Write updated quotes to json file
      output_filename = filename[:-9] + "_updated.json.bz2"   # change to just filename when sure
      with bz2.open(output_filename, 'wb') as bzoutput:
          df.to_json(bzoutput)
      
      
#filter_quotes_with_BERT("generated/2016/", ["drowning"])








