from keyword import Keyword
import pandas as pd

PATH_TO_KEYWORDS_FILE = "./data/keywords.txt"


class Topics:
    quotes_occurences_df: pd.DataFrame = []
    keywords = []


    def get_keyword_by_name(self, name) -> Keyword:
        for k in self.keywords:
            if k.name == name:
                return k

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


    def __init__(self, name: str, keywords: []):
        self.name = name
        self.keywords = keywords

