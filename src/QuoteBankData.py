"""
File name: QuoteBankData.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

from src.Keyword import Keyword
from src.CONSTS import KEYWORDS_FILE_PATH, GENERATED_PATH
import quotebank_preprocessing_utils as utils
import pandas as pd
import json
import sys


#TODO: change class name
class QuoteBankData:

    def __init__(self, name: str, keywords: []):
        self.name = name
        self.keywords = keywords
        self.quotes_occurrences_df = pd.DataFrame()

    def get_all_keyword_names(self) -> list:
        """
        Get all keyword names for the topic
        :return: A list of all keyword names
        """
        all_keyword_names = []
        for k in self.keywords:
            all_keyword_names.append(k.name)
        return all_keyword_names

    def get_keyword_by_name(self, name) -> Keyword:
        """
        Given name return the corresponding Keyword object from self.keyword list
        :param name: str
        :return: Keyword
        """
        for k in self.keywords:
            if k.name == name:
                return k

    def read_keywords_from_file(self):
        """
        Open keywords.txt, parse every line according to diamond operator (<>)
        The first element of the line parsed gets assigned to keyword name, whereas the following will be considered
        as synonyms
        """
# =============================================================================
#         
#         with open(KEYWORDS_FILE_PATH, "r") as file:
#             textfile = file.readlines()
# 
#             for i, line in enumerate(textfile):
#                 lowercase_line = line.lower()
#                 keywords_line = lowercase_line.replace("\n", "").split("<>")
#                 self.keywords.append(Keyword(keywords_line[0]))
#                 self.keywords[i].synonym = keywords_line[1:]
#                 
# =============================================================================
        with open(KEYWORDS_FILE_PATH[-3] + "json", "r") as file:
            
          keywords = json.load(file)
          
          for i, key in enumerate(keywords.keys()):
            self.keywords.append(Keyword(key))
            self.keywords[i].synonym = keywords[key]
        
        

    def match_quotation_with_any_keyword(self, quotation) -> [Keyword]:
        """
        Given a quotation return the matching keyword, if any
        :param quotation: str
        :return: Keyword
        """
        found_keywords = []
        for k in self.keywords:
            if k.find_keyword_in_quotation(quotation):
                found_keywords.append(k)
        return found_keywords

    def write_matching_quotes_to_file_for_year(self, year_index):
        """
        For each keyword, write matched quotes to respective json file (for that keyword, and year)
        :param year_index: int
        """
        # TODO from speaker and URL --> add json parameter for country
        for k in self.keywords:
            k.assign_quote_to_file_for_year(year_index)

    def delete_json_lines_for_all_keywords(self):
        """
        Clear all the json_lines associated to every keyword
        """
        for k in self.keywords:
            k.json_lines.clear()

    def create_json_dumps_filenames_for_each_keyword(self):
        """
        For each keyword create all the json file names associated to it
        """
        years_for_file = utils.get_all_years()

        for k in self.keywords:
            for year in years_for_file:
                directory_for_year = year + "/"
                relative_path_for_file_for_year = utils.format_filenames_nicely(k.name) + "-" + year + ".json.bz2"
                k.output_filenames.append(GENERATED_PATH + directory_for_year + relative_path_for_file_for_year)

    def print_pretty_keywords(self):
        """
        Print all keyword names and associated synonyms in a nice format
        """
        for tk in self.keywords:
            print("\nPrinting keyword")
            print(tk.name)
            for i, tks in enumerate(tk.synonym):
                if i == 0:
                    print("Printing synonyms")
                print("\t" + tks)

    def print_pretty_keywords_filenames(self):
        """
        For each keyword, print all the associated json filenames
        """
        for tk in self.keywords:
            print("\nPrinting keyword")
            print(tk.name)
            for i, tks in enumerate(tk.output_filenames):
                if i == 0:
                    print("Printing filenames")
                print("\t" + tks)
