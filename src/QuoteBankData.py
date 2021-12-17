"""
File name: QuoteBankData.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

from src.Keyword import Keyword
from src.CONSTS import *
from src.utilities import quotebank_preprocessing_utils as utils
from src.utilities import string_utils as str_utils
import pandas as pd
import json
import numpy as np

# TODO: change class name
class QuoteBankData:

    def __init__(self, name: str, keywords: list):
        self.name = name
        self.keywords = keywords
        self.quotes_occurrences_df = pd.DataFrame(columns=["Year"] + TOPICS)
        self.quotes_percentage_df = self.quotes_occurrences_df.copy()
        self.cat_quotes_occurrences_df = pd.DataFrame(columns=["Year"] + CATEGORIES)
        self.cat_quotes_percentage_df = self.cat_quotes_occurrences_df.copy()


    def read_keywords_from_file(self):
        """
        Open keywords.txt, parse every line according to diamond operator (<>)
        The first element of the line parsed gets assigned to keyword name, whereas the following will be considered
        as synonyms
        """

        with open(KEYWORDS_JSON_FILE_PATH, "r") as file:
            keywords_json_list = json.load(file)

            for i, key in enumerate(keywords_json_list.keys()):
                self.keywords.append(Keyword(key.capitalize()))
                self.keywords[i].synonym = keywords_json_list[key]


    def match_quotation_with_any_keyword(self, quotation) -> list:
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
      
      
    def sample_found_quotes(self, year_index, output_name):
        """
        For each keyword, samples found quotes and writes to text file.
        Ten random quotes are taken.
        :param year_index: int
               output_name: str
        """
        # Get sample list
        sample = list()
        for k in self.keywords:
            if len(k.json_lines) > 10:
                sample.extend(k.get_sample_of_found_quotes())
                
        # write list to file
        if sample:
            years = utils.get_all_years()   
            output =  GENERATED_PATH + years[year_index] + "/" + output_name
            with open(output, 'w+', encoding="utf-8") as the_file:
                for element in sample:
                    the_file.write(element + "\n")  
    
    
    def filter_found_quotes_by_clustering(self):
        """After the quotes have been found in the data base for a year, do an extra 
        filtering step by clustering."""
        for k in self.keywords:
            if k.name in TOPICS_FOR_CLUSTERING and len(k.json_lines) > 100:
                k.filter_quotes()
      

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
                relative_path_for_file_for_year = str_utils.format_filenames_nicely(k.name) + "-" + year + ".json.bz2"
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


    def map_df_causes_to_categories(self):
        cause_df = self.quotes_occurrences_df.copy()
        self.cat_quotes_occurrences_df["Year"] = cause_df["Year"]
        
        for cat_col in self.cat_quotes_occurrences_df.columns:
            if cat_col in DEATHS_INFO_COLUMNS: continue
            
            cat_values = np.zeros(cause_df.shape[0])
            
            for cause_col in CATEGORY_MAPPING[cat_col]:
                cat_values += cause_df[cause_col].to_numpy()
            self.cat_quotes_occurrences_df[cat_col] = cat_values
            
    
    def get_quote_occurences_per_country_year(self, url_or_speaker):
        """This function returns the number of quotes from a country per year, based on speaker or url.
        param: url_or_speaker: str
        return: totals_per_country: dict, keys are like (country,year)"""

        # Check value
        if url_or_speaker != "url" and url_or_speaker != "speaker":
            raise ValueError("Did not choose url or speaker")

        # Safe variable
        totals_per_country = dict()
        # Get occurences form url from countries
        if url_or_speaker == "url":
            for i in range(len(self.keywords)):   
                for key in self.keywords[i].country_url_occurences:
                    if key in totals_per_country:
                        totals_per_country[key] += self.keywords[i].country_url_occurences[key]
                    else:
                        totals_per_country[key] = self.keywords[i].country_url_occurences[key]
        # Get occurences of speakers from countries              
        elif url_or_speaker == "speaker":
            for i in range(len(self.keywords)):   
                for key in self.keywords[i].country_speaker_occurences:
                    if key in totals_per_country:
                        totals_per_country[key] += self.keywords[i].country_speaker_occurences[key]
                    else:
                        totals_per_country[key] = self.keywords[i].country_speaker_occurences[key]

        return totals_per_country


    def get_country_per_year_count(self, url_or_speaker, countries, year, percentage = False):
        # Check value
        if url_or_speaker != "url" and url_or_speaker != "speaker":
            raise ValueError("Did not choose url or speaker")

        # Initialize output
        topic_appearance_country = np.zeros((len(self.keywords), len(countries)+1)) # Last column for rest of the world
        topics = list()
        for i in range(len(self.keywords)):
            topics.append(self.keywords[i].name)
            if url_or_speaker == "url":
                for key in self.keywords[i].country_url_occurences:
                    if key[0] in countries and key[1] == year:
                        topic_appearance_country[i, countries.index(key[0])] = self.keywords[i].country_url_occurences[key]
                    elif key[0] is not None and key[1] == year:
                        topic_appearance_country[i, -1] += self.keywords[i].country_url_occurences[key] # rest of the World

            elif url_or_speaker == "speaker":
                for key in self.keywords[i].country_speaker_occurences:
                    if key[0] in countries and key[1] == year:
                        topic_appearance_country[i, countries.index(key[0])] = self.keywords[i].country_speaker_occurences[key]
                    elif key[0] is not None and key[1] == year:
                        topic_appearance_country[i, -1] += self.keywords[i].country_speaker_occurences[key] # rest of the World

        # Make into DataFrame
        topic_appearance_country = np.transpose(topic_appearance_country)
        topic_appearance_country = pd.DataFrame(data = topic_appearance_country,
                                               columns = topics)

        return topic_appearance_country
