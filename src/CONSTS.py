"""
File name: CONSTS.py
Author: HOJA
Date created: 12/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

DATA_PATH = './data/'
GENERATED_PATH = './generated/'
KEYWORDS_FILE_PATH = DATA_PATH + "keywords.txt"
KEYWORDS_JSON_FILE_PATH = DATA_PATH + "keywords.json"
COUNTRY_EXTENSIONS_FILE_PATH = DATA_PATH + "country_url_end.txt"
SPEAKER_ATTRIBUTES_PATH = DATA_PATH + "speaker_attributes.parquet"

COLORS = ["red", "green", "blue", "brown", "yellow", "purple", "orange", "pink"]

TOPICS_FOR_CLUSTERING =  ["fire, heat, and hot substances",
                          "environmental heat and cold exposure",
                          "road injuries",
                          "war and terrorism",
                          "interpersonal violence",
                          "poisonings",
                          "drowning"]

COUNTRY_IDENTIFIER = dict()
SPEAKER_ATTRIBUTES = dict()

BEGIN_YEAR = 2008
END_YEAR = 2017

# Deaths object constants
DEATHS_INFO_COLUMNS = ["Entity", "Code", "Year"]
