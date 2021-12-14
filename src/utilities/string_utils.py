"""
File name: string_utils.py
Author: HOJA
Date created: 14/12/2021
Date last modified: 14/12/2021
Python Version: 3.8
"""

import json
from src.CONSTS import SPECIAL_CHARS


def format_filenames_nicely(filename) -> str:
    """
    Replace any occurrences of unwanted characters in filenames, according to a specific format
    :param filename: str
    :return: str
    """

    for special_char in SPECIAL_CHARS:
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


def extract_quotation(line) -> str:
    """
    Return the quotation from a parsed json
    :param line: str
    :return: str
    """
    json_line = json.loads(line)
    return json_line['quotation']
