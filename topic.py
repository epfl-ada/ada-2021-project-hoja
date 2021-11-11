#from keyword import Keyword
import pandas as pd
import json
from thefuzz import fuzz

PATH_TO_KEYWORDS_FILE = "./data/keywords.txt"

class Keyword:

    def __init__(self, name):
        self.name = name
        self.quotes = pd.DataFrame(columns = ["quoteID", "quotation", "speaker", "qids", "date", "numOccurrences", "probas", "urls", "phase"])
        self.synonym = []
    
    def find_keyword_in_quotation(self, quotation) -> bool:
        for syn in self.synonym:
            if fuzz.partial_ratio(quotation, syn) > (100 - len(syn)):
                return True
        return False

class Topics:

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
                keywords_line = line.replace("\n", "").split("<>")
                self.keywords.append(Keyword(keywords_line[0]))
                self.keywords[i].synonym = keywords_line[1:]

    def print_pretty_keywords(self):
        for tk in self.keywords:
            print("\nPrinting keyword")
            print(tk.name)
            for i, tks in enumerate(tk.synonym):
                if i == 0: print("Printing synonyms")
                print("\t" + tks)
               
    def match_quotation_with_any_keyword(self, quotation) -> Keyword:
        for k in self.keywords:
            if k.find_keyword_in_quotation(quotation):
                return k


    def __init__(self, name: str, keywords: []):
        self.name = name
        self.keywords = keywords
        self.quotes_occurences_df = pd.DataFrame()

