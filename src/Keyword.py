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
            if len(syn.split(" ")) == 1:
                if syn in lowercase_quotation_list:
                    return True
            else:
                if syn in lowercase_quotation:
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

    def print_pretty_json_lines_info(self):
        """
        Print keyword name and number of matched json lines from quotebank files
        """
        print(self.name)
        print("\t %d" % len(self.json_lines))