"""
File name: CONSTS.py
Author: HOJA
Date created: 12/11/2021
Date last modified: 17/12/2021
Python Version: 3.8
"""
import matplotlib.pyplot as plt

# File Paths
DATA_PATH = './data/'
GENERATED_PATH = './generated/'
GENERATED_IMAGES_PATH = GENERATED_PATH + "images/"
KEYWORDS_FILE_PATH = DATA_PATH + "keywords.txt"
KEYWORDS_JSON_FILE_PATH = DATA_PATH + "keywords.json"
COUNTRY_EXTENSIONS_FILE_PATH = DATA_PATH + "country_url_end.txt"
SPEAKER_ATTRIBUTES_PATH = DATA_PATH + "speaker_attributes.parquet"
URL_END_PATH = DATA_PATH + "country_url_end.txt"
URL_COUNTRY_PATH = DATA_PATH + "url_country_lib.json"
ID_COUNTRY_PATH = DATA_PATH +  "id_country_lib.json"

# Causes
ALZHEIMER_DISEASE_AND_OTHER_DEMENTIAS = 'Alzheimer disease and other dementias'
CARDIOVASCULAR_DISEASES = 'Cardiovascular diseases'
CHRONIC_KIDNEY_DISEASE = 'Chronic kidney disease'
CHRONIC_RESPIRATORY_DISEASES =  'Chronic respiratory diseases'
CIRRHOSIS_AND_OTHER_CHRONIC_LIVER_DISEASES = 'Cirrhosis and other chronic liver diseases'
DIABETES_MELLITUS = 'Diabetes mellitus'
DIARRHEAL_DISEASES = 'Diarrheal diseases'
DIGESTIVE_DISEASES = 'Digestive diseases'
DROWNING = 'Drowning'
DRUG_USE_AND_ALCOHOLISM = 'Drug use and alcoholism'
EXPOSURE_TO_FORCES_OF_NATURE = 'Exposure to forces of nature'
FIRE_HEAT_AND_HOT_SUBSTANCES = 'Fire, heat, and hot substances'
HEPATITIS = 'Hepatitis'
HIV_AIDS = 'Hiv/aids'
INTERPERSONAL_VIOLENCE = 'Interpersonal violence'
INTESTINAL_INFECTIOUS_DISEASES = 'Intestinal infectious diseases'
LOWER_RESPIRATORY_INFECTIONS = 'Lower respiratory infections'
MALARIA = 'Malaria'
MATERNAL_DISORDERS = 'Maternal disorders'
MENINGITIS = 'Meningitis'
NEONATAL_DISORDERS = 'Neonatal disorders'
NEOPLASMS = 'Neoplasms'
NUTRITIONAL_DEFICIENCIES = 'Nutritional deficiencies'
PARKINSON_DISEASE = 'Parkinson disease'
POISONINGS = 'Poisonings'
ROAD_INJURIES = 'Road injuries'
SUICIDE = 'Suicide'
TUBERCULOSIS = 'Tuberculosis'
WAR_AND_TERRORISM = 'War and terrorism'

TOPICS = [ALZHEIMER_DISEASE_AND_OTHER_DEMENTIAS, 
          CARDIOVASCULAR_DISEASES, 
          CHRONIC_KIDNEY_DISEASE, 
          CHRONIC_RESPIRATORY_DISEASES, 
          CIRRHOSIS_AND_OTHER_CHRONIC_LIVER_DISEASES,
          DIABETES_MELLITUS,
          DIARRHEAL_DISEASES,
          DIGESTIVE_DISEASES, 
          DROWNING, 
          DRUG_USE_AND_ALCOHOLISM, 
          EXPOSURE_TO_FORCES_OF_NATURE, 
          FIRE_HEAT_AND_HOT_SUBSTANCES, 
          HEPATITIS, 
          HIV_AIDS,
          INTERPERSONAL_VIOLENCE, 
          INTESTINAL_INFECTIOUS_DISEASES, 
          LOWER_RESPIRATORY_INFECTIONS, 
          MALARIA, 
          MATERNAL_DISORDERS, 
          MENINGITIS, 
          NEONATAL_DISORDERS, 
          NEOPLASMS, 
          NUTRITIONAL_DEFICIENCIES, 
          PARKINSON_DISEASE, 
          POISONINGS, 
          ROAD_INJURIES, 
          SUICIDE, 
          TUBERCULOSIS, 
          WAR_AND_TERRORISM]

# Regular expression chars
SPECIAL_CHARS = "!#$%^&*()/ "

# Colors
COLORS = ["003F5C", "2F4B7C", "665191", "A05195", "D45087", "F95D6A", "FF7C43", "FF600"]
COLOR_MAP = plt.get_cmap('tab20c')

# Topics for clustering
TOPICS_FOR_CLUSTERING = [FIRE_HEAT_AND_HOT_SUBSTANCES,
                         EXPOSURE_TO_FORCES_OF_NATURE,
                         ROAD_INJURIES,
                         WAR_AND_TERRORISM,
                         INTERPERSONAL_VIOLENCE,
                         POISONINGS,
                         DROWNING]

# Keyword Stopword
KEYWORD_STOPWORDS = ['consumption',
                     'piles',
                     'intoxication',
                     'the base']

KEYWORD_DIABETES_TYPE2 = 'diabetes mellitus'
KEYWORD_POISONING = POISONINGS
KEYWORD_POISONING_EXTENSIONS = ["lead", "water", "food", "arsenic"]

SYNONYM_DICTIONARY = {
        "stroke": "stroke.n.03",
        "aids": "AIDS.n.01",
        "fire": "fire.n.01",
        "consumption": "pulmonary_tuberculosis.n.01"
}

# Years for data processing
BEGIN_YEAR = 2008
END_YEAR = 2016

# Deaths object constants
DEATHS_INFO_COLUMNS = ["Entity", "Code", "Year"]
COMBINED_COLS = {WAR_AND_TERRORISM: ["Conflict and terrorism", "Terrorism"], 
                 EXPOSURE_TO_FORCES_OF_NATURE: [EXPOSURE_TO_FORCES_OF_NATURE, "Environmental heat and cold exposure"],
                 NUTRITIONAL_DEFICIENCIES: [NUTRITIONAL_DEFICIENCIES, "Protein-energy malnutrition"],
                 DRUG_USE_AND_ALCOHOLISM: ["Drug use disorders", "Alcohol use disorders"]}
RENAME_CAUSE_COLS = {'Terrorism (deaths)': 'Terrorism', 'Deaths - Self-harm - Sex: Both - Age: All Ages (Number)': 'Suicide'}
DROP_CAUSE_COLS = ['Number of executions (Amnesty International)']

# Categories
INJURIES = "Injuries"
NON_COMMUNICABLE_DISEASES = "Non-communicable diseases"
COMMUNICABLE_DISEASES = "Communicable diseases"
RENAME_CAT_COLS = {"Deaths - Communicable, maternal, neonatal, and nutritional diseases - Sex: Both - Age: All Ages (Number)": COMMUNICABLE_DISEASES}

CATEGORIES = [INJURIES, NON_COMMUNICABLE_DISEASES, COMMUNICABLE_DISEASES]
CATEGORY_MAPPING = {INJURIES: [FIRE_HEAT_AND_HOT_SUBSTANCES, ROAD_INJURIES, WAR_AND_TERRORISM, EXPOSURE_TO_FORCES_OF_NATURE, DROWNING, SUICIDE, INTERPERSONAL_VIOLENCE, POISONINGS,  DRUG_USE_AND_ALCOHOLISM], 
                    NON_COMMUNICABLE_DISEASES: [DIGESTIVE_DISEASES, ALZHEIMER_DISEASE_AND_OTHER_DEMENTIAS, PARKINSON_DISEASE, CARDIOVASCULAR_DISEASES, DIABETES_MELLITUS, CHRONIC_RESPIRATORY_DISEASES, CHRONIC_KIDNEY_DISEASE, NEOPLASMS, CIRRHOSIS_AND_OTHER_CHRONIC_LIVER_DISEASES],
                    COMMUNICABLE_DISEASES: [MENINGITIS, LOWER_RESPIRATORY_INFECTIONS, HEPATITIS, DIARRHEAL_DISEASES, NEONATAL_DISORDERS, NUTRITIONAL_DEFICIENCIES, MATERNAL_DISORDERS, HIV_AIDS, MALARIA, TUBERCULOSIS, INTESTINAL_INFECTIOUS_DISEASES]}


# Country and region consts
ALL_COUNTRIES_CODE = ['af', 'ax', 'al', 'dz', 'as', 'ad', 'ao', 'ai', 'aq', 'ag', 'ar', 'am', 'aw', 'au', 'at', 'az',
                    'bs', 'bh', 'bd', 'bb', 'by', 'be', 'bz', 'bj', 'bm', 'bt', 'bo', 'bq', 'ba', 'bw', 'bv', 'br', 'io',
                    'bn', 'bg', 'bf', 'bi', 'kh', 'cm', 'ca', 'cv', 'ky', 'cf', 'td', 'cl', 'cn', 'cx', 'cc', 'co', 'km',
                    'cg', 'cd', 'ck', 'cr', 'ci', 'hr', 'cu', 'cw', 'cy', 'cz', 'dk', 'dj', 'dm', 'do', 'ec', 'eg', 'sv',
                    'er', 'ee', 'et', 'fk', 'fo', 'fj', 'fi', 'fr', 'gf', 'pf', 'tf', 'ga', 'gm', 'ge', 'de', 'gh', 'gi',
                    'gr', 'gl', 'gd', 'gp', 'gu', 'gt', 'gg', 'gn', 'gw', 'gy', 'ht', 'hm', 'va', 'hn', 'hk', 'hu', 'is',
                    'in', 'id', 'ir', 'iq', 'ie', 'im', 'il', 'it', 'jm', 'jp', 'je', 'jo', 'kz', 'ke', 'ki', 'kp', 'kr',
                    'kw', 'kg', 'la', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', 'mo', 'mk', 'mg', 'mw', 'my', 'mv',
                    'ml', 'mt', 'mh', 'mq', 'mr', 'mu', 'yt', 'mx', 'fm', 'md', 'mc', 'mn', 'me', 'ms', 'ma', 'mz', 'mm',
                    'na', 'nr', 'np', 'nl', 'nc', 'nz', 'ni', 'ne', 'ng', 'nu', 'nf', 'mp', 'no', 'om', 'pk', 'pw', 'ps',
                    'pa', 'pg', 'py', 'pe', 'ph', 'pn', 'pl', 'pt', 'pr', 'qa', 're', 'ro', 'ru', 'rw', 'bl', 'sh', 'kn',
                    'lc', 'mf', 'pm', 'vc', 'ws', 'sm', 'st', 'sa', 'sn', 'rs', 'sc', 'sl', 'sg', 'sx', 'sk', 'si', 'sb',
                    'so', 'za', 'gs', 'ss', 'es', 'lk', 'sd', 'sr', 'sj', 'sz', 'se', 'ch', 'sy', 'tw', 'tj', 'tz', 'th',
                    'tl', 'tg', 'tk', 'to', 'tt', 'tn', 'tr', 'tm', 'tc', 'tv', 'ug', 'ua', 'ae', 'gb', 'us', 'um', 'uy',
                    'uz', 'vu', 've', 'vn', 'vg', 'vi', 'wf', 'eh', 'ye', 'zm', 'zw', 'gq']

REGIONS = ['Latin America and Caribbean','North Africa and Middle East','Sub-Saharan Africa','Oceania','Central Asia', 'East Asia','South Asia', 'Southeast Asia','Central Europe',"Eastern Europe", 'Western Europe',  'United States','Canada']

MAIN_REGIONS = {'Latin America': ['Latin America and Caribbean'],
                'North America': ['United States','Canada'],
                'Europe': ['Central Europe',"Eastern Europe", 'Western Europe'],
                'Sub-Saharan Africa': ['Sub-Saharan Africa'],
                'North Africa and Middle East': ['North Africa and Middle East'],
                'Asia':['Central Asia', 'East Asia','South Asia', 'Southeast Asia'],
                'Oceania': ['Oceania']}
# To add country of speaker
COUNTRY_IDENTIFIER = dict()
SPEAKER_ATTRIBUTES = dict()
# To add country of url
URL_END_LIB = dict()
URL_COUNTRY = dict()
