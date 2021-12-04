"""
File name: quotebank_preprocessing_utils.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

import os
import json
from src.CONSTS import DATA_PATH, GENERATED_PATH, BEGIN_YEAR, END_YEAR

begin_year = BEGIN_YEAR - 2000
end_year = (END_YEAR - 2000) + 1


def compose_quotebank_filenames() -> list:
    """
    Compose all the quotebank filenames to be read
    :return: list
    """
    quotes_file_list = []
    for i in range(begin_year, end_year):
        year = create_year_string_from_number(i)
        quotes_file_list.append(DATA_PATH + "quotes-" + year + ".json.bz2")
    return quotes_file_list


def create_directories_for_every_year():
    """
    For each year, create the corresponding directory where all the output files of each keyword will be stored
    """
    for i in range(begin_year, end_year):
        year = create_year_string_from_number(i)
        path = GENERATED_PATH + year + "/"
        os.makedirs(path, exist_ok = True)

# TODO: create utils file for only managing strings called: string_utils.py


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
    for i in range(begin_year, end_year):
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
