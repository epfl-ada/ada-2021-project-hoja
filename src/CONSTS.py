"""
File name: CONSTS.py
Author: HOJA
Date created: 12/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""

# File Paths
DATA_PATH = './data/'
GENERATED_PATH = './generated/'
KEYWORDS_FILE_PATH = DATA_PATH + "keywords.txt"
KEYWORDS_JSON_FILE_PATH = DATA_PATH + "keywords.json"
COUNTRY_EXTENSIONS_FILE_PATH = DATA_PATH + "country_url_end.txt"
SPEAKER_ATTRIBUTES_PATH = DATA_PATH + "speaker_attributes.parquet"
URL_END_PATH = DATA_PATH + "country_url_end.txt"
URL_COUNTRY_PATH = DATA_PATH + "url_country_lib.json"

# Colors
COLORS = ["red", "green", "blue", "brown", "yellow", "purple", "orange", "pink"]

# Topics for clustering
TOPICS_FOR_CLUSTERING = ["Fire, heat, and hot substances",
                          "Environmental heat and cold exposure",
                          "Road injuries",
                          "War and terrorism",
                          "Interpersonal violence",
                          "Poisonings",
                          "Drowning"]

# Keyword Stopword
KEYWORD_STOPWORDS = ['consumption',
                     'piles',
                     'intoxication',
                     'the base']

KEYWORD_DIABETES_TYPE2 = 'Diabetes mellitus'

# To add country of speaker
COUNTRY_IDENTIFIER = dict()
SPEAKER_ATTRIBUTES = dict()

# To add country of url
URL_END_LIB = dict()
URL_COUNTRY = dict()

# Years for data processing
BEGIN_YEAR = 2009
END_YEAR = 2011

# Deaths object constants
DEATHS_INFO_COLUMNS = ["Entity", "Code", "Year"]
COMBINED_COLS = {"War and terrorism": ["Conflict and terrorism", "Terrorism"], 
                 "Exposure to forces of nature": ["Exposure to forces of nature", "Environmental heat and cold exposure"],
                 "Nutritional deficiencies": ["Nutritional deficiencies", "Protein-energy malnutrition"],
                 "Drug use and alcoholism": ["Drug use disorders", "Alcohol use disorders"]}
