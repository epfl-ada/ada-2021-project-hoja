#from keyword import Keyword
import pandas as pd
import json
from thefuzz import fuzz
import os.path
import bz2

PATH_TO_KEYWORDS_FILE = "./data/keywords.txt"
PATH = "./data/"

class Keyword:

    def __init__(self, name):
        self.name = name
        self.output_filenames = []
        self.json_quotes = []
        self.quotes = pd.DataFrame(columns = ["quoteID", "quotation", "speaker", "qids", "date", "numOccurrences", "probas","urls","phase"])
        self.synonym = []
    
    def find_keyword_in_quotation(self, quotation) -> bool:
#         for syn in self.synonym:
        lowercase_quotation = quotation.lower()
        lowercase_quotation_list = lowercase_quotation.split(" ")
        # print(lowercase_quotation)
        # print(lowercase_quotation_list)
        for syn in self.synonym:
            threshold = 100 - len(syn)
            if len(syn.split(" ")) == 1:
                if syn in lowercase_quotation_list:
                    return True
            else:
                if syn in lowercase_quotation:
                    return True
        return False

        

class Topics:

    def get_all_keyword_names(self) -> list:
        all_keyword_names = []
        for k in self.keywords:
            all_keyword_names.append(k.name)
        return all_keyword_names

    def get_keyword_by_name(self, name) -> Keyword:
        for k in self.keywords:
            if k.name == name:
                return k
    
    def assign_keyword(self, found_keyword, line):
        key = self.get_keyword_by_name(found_keyword.name)
        key.quotes = key.quotes.append(
                    json.loads(line),
                    ignore_index = True)

    def read_keywords_from_file(self):
        with open(PATH_TO_KEYWORDS_FILE, "r") as file:
            textfile = file.readlines()

            for i, line in enumerate(textfile):
                lowercase_line = line.lower()
                keywords_line = lowercase_line.replace("\n", "").split("<>")
                self.keywords.append(Keyword(keywords_line[0]))
                self.keywords[i].synonym = keywords_line[1:]

    def print_pretty_keywords(self):
        for tk in self.keywords:
            print("\nPrinting keyword")
            print(tk.name)
            for i, tks in enumerate(tk.synonym):
                if i == 0: print("Printing synonyms")
                print("\t" + tks)

    def print_pretty_keywords_years(self):
        for tk in self.keywords:
            print("\nPrinting keyword")
            print(tk.name)
            for i, tks in enumerate(tk.output_filenames):
                if i == 0: print("Printing filenames")
                print("\t" + tks)
               
    def match_quotation_with_any_keyword(self, quotation) -> Keyword:
        for k in self.keywords:
            if k.find_keyword_in_quotation(quotation):
                return k
    
    def assign_quote_to_file(self, keyword, index, line):
        key = self.get_keyword_by_name(keyword)
        with bz2.open(key.output_filenames[index], 'wb') as output_file:
            output_file.write((json.dumps(json.loads(line))+'\n').encode('utf-8'))
        output_file.close()


    def __init__(self, name: str, keywords: []):
        self.name = name
        self.keywords = keywords
        self.quotes_occurences_df = pd.DataFrame()

