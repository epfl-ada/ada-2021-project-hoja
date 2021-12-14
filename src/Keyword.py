"""
File name: Keyword.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

import pandas as pd
import json
import bz2
import numpy as np
from numpy import ndarray

from src.utilities import quotebank_preprocessing_utils as utils
from src.utilities import cluster_quotes_BERT as BERT
from src.CONSTS import KEYWORD_POISONING, KEYWORD_POISONING_EXTENSIONS


class Keyword:

    def __init__(self, name):
        self.name = name
        self.output_filenames = []
        self.json_lines = []
        self.quotes = pd.DataFrame(
            columns=["quoteID", "quotation", "speaker", "qids", "date", "numOccurrences", "probas", "urls", "phase"])
        self.synonym = []

    def find_keyword_in_quotation(self, quotation) -> bool:
        """
        Given a quotation assess if the keyword or one of its synonyms are there. Return True if found, False otherwise
        :param quotation: str
        :return: bool
        """
        lowercase_quotation = quotation.lower()
        lowercase_quotation_list = lowercase_quotation.split(" ")
        for syn in self.synonym:
            syn = syn.split(" ")
            if set(syn).issubset(lowercase_quotation_list):
                return True

        return False

    def assign_quote_to_file_for_year(self, year_index):
        """
        For a single keyword, open the corres
        :param year_index:
        """
        with bz2.open(self.output_filenames[year_index], 'wb') as output_file:
            for line in self.json_lines:
                output_file.write((json.dumps(json.loads(line)) + '\n').encode('utf-8'))
        output_file.close()

    def get_sample_of_found_quotes(self, n=10):
        """"Get a sample of size n of the found quotes."""
        quotes = list()  # Extract quotes from matched json lines
        for line in self.json_lines:
            quotes.append(utils.extract_quotation(line))

        if len(quotes) > n:  # Take a random subset of the quotes
            indices = np.random.randint(0, len(quotes), n)
            sample = [self.name]
            for index in indices:
                sample.append(quotes[index])
            sample.append("\n")
            return sample

    def filter_quotes(self):
        """
        The quotes are updated by vectorizing the quotes with SentenceTransformers
        and clustering with HDBSCAN.
        Clusters for which at least two of the ten most important words are in the keywords
        are kept.
        """

        quotes = list()
        for line in self.json_lines:
            quotes.append(utils.extract_quotation(line))

        # cluster data
        cluster = BERT.cluster_quotes(quotes)

        # Keep the right clusters
        print("assigning ...")
        quotes_df = pd.DataFrame(quotes, columns=["quotation"])
        quotes_df['Topic'] = cluster.labels_
        quotes_per_topic = quotes_df.groupby(['Topic'], as_index=False).agg({'quotation': ' '.join})

        tf_idf, count = BERT.c_tf_idf(quotes_per_topic.quotation.values, m=len(quotes))
        # Get top 10 words per topic
        top_n_words = BERT.extract_top_n_words_per_topic(tf_idf, count, quotes_per_topic, n=10)
        # Get topics which have at least 2 words in their top 10 which are also in the keyword list
        keywords = self.synonym
        if self.name == KEYWORD_POISONING:
            keywords.extend(KEYWORD_POISONING_EXTENSIONS)

        correct_clusters = BERT.select_correct_topics(top_n_words, keywords)

        # Get indices of correct quotes
        lines_to_keep: ndarray = np.zeros(len(quotes_df), dtype=bool)
        for cluster in correct_clusters:
            lines_to_keep = np.logical_or(lines_to_keep, quotes_df['Topic'] == cluster)

        self.json_lines = np.array(self.json_lines)[lines_to_keep].tolist()

    def print_pretty_json_lines_info(self):
        """
        Print keyword name and number of matched json lines from quotebank files
        """
        print(self.name)
        print("\t %d" % len(self.json_lines))
