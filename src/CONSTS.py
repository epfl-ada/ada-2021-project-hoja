"""
File name: CONSTS.py
Author: HOJA
Date created: 12/11/2021
Date last modified: 12/11/2021
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

# To add country of speaker
COUNTRY_IDENTIFIER = dict()
SPEAKER_ATTRIBUTES = dict()

# To add country of url
URL_END_LIB = dict()
URL_COUNTRY = dict()

# Years for data processing
BEGIN_YEAR = 2008
END_YEAR = 2017

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

