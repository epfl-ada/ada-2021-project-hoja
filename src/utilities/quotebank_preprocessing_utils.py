"""
File name: quotebank_preprocessing_utils.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

import os
import json
from src.CONSTS import BEGIN_YEAR, END_YEAR, DATA_PATH, GENERATED_PATH, SPEAKER_ATTRIBUTES_PATH, SPEAKER_ATTRIBUTES, URL_END_PATH, URL_END_LIB, URL_COUNTRY_PATH, URL_COUNTRY
from src.utilities import string_utils as str_utils
import pandas as pd

begin_year = BEGIN_YEAR - 2000
end_year = (END_YEAR - 2000) + 1


def compose_quotebank_filenames() -> list:
    """
    Compose all the quotebank filenames to be read
    :return: list
    """
    quotes_file_list = []
    for i in range(begin_year, end_year):
        year = str_utils.create_year_string_from_number(i)
        quotes_file_list.append(DATA_PATH + "quotebank/" + "quotes-" + year + ".json.bz2")
    return quotes_file_list


def create_directories_for_every_year():
    """
    For each year, create the corresponding directory where all the output files of each keyword will be stored
    """
    for i in range(begin_year, end_year):
        year = str_utils.create_year_string_from_number(i)
        path = GENERATED_PATH + year + "/"
        os.makedirs(path, exist_ok = True)


def get_all_years() -> list:
    """
    Get a list all of the years, for the files to be read
    :return: list
    """
    years_for_file = []
    for i in range(begin_year, end_year):
        year = str_utils.create_year_string_from_number(i)
        years_for_file.append(year)

    return years_for_file


def load_speaker_info():
    """
    Load speaker info from parquet file into dataframe. Then remove useless stuff.
    Finally transform into dict, since lookup will be faster. Keys are speaker id and
    values for keys are the country ids.
    """
    print("Load speaker info...")
    raw_df = pd.read_parquet(SPEAKER_ATTRIBUTES_PATH)
    raw_df = raw_df[raw_df['nationality'].notna()]
    raw_df = raw_df[raw_df['date_of_birth'].notna()]     
    raw_df = raw_df.reset_index()
    dates = raw_df['date_of_birth'].tolist()
    raw_df = raw_df[['nationality','id']]
                    
    for i in range(len(dates)):
        if int(dates[i][0][1:5]) > 1920:   
            SPEAKER_ATTRIBUTES[raw_df['id'][i]] = raw_df['nationality'][i]
    
    return SPEAKER_ATTRIBUTES


def load_url_end():
    file = open(URL_END_PATH, "r")
    for index, line in enumerate(file):
        URL_END_LIB[line[:-1].split('\t')[1][1:]] = line[:-1].split('\t')[0]


def load_url_country_lib():
    if os.path.isfile(URL_COUNTRY_PATH):
        with open(URL_COUNTRY_PATH, 'r') as fp:
            inter = json.load(fp)
        for key in inter:
            URL_COUNTRY[key] = inter[key]


def safe_url_country_lib():
    with open(URL_COUNTRY_PATH, 'w+') as fp:
        json.dump(URL_COUNTRY, fp)
