import os
import bz2
from src.QuoteBankData import QuoteBankData
from src.CONSTS import KEYWORDS_FILE_PATH, KEYWORDS_JSON_FILE_PATH
from src.utilities import quotebank_preprocessing_utils as utils
from src.utilities import synonym_utils as syn_utils
from src.utilities import add_country_speaker as country_utils
from tqdm import tqdm
import json
import pandas as pd

def quotation_classification():
    """
    Iterate through all quotebank files, stored locally. For each quote inside the file, check which keywords match.
    Store the results in the respective output
    """
    quotes_filenames_list = utils.compose_quotebank_filenames()

    for index, filename in enumerate(quotes_filenames_list):
        print("Elaborating file: " + filename.split("/").pop())
        quotation_classification_for_file(filename)
        quotebank.sample_found_quotes(index, "before.txt") #Sample quotes found
        quotebank.filter_found_quotes_by_clustering() # Cluster some topics and remove wrong quotes
        
        quotebank.sample_found_quotes(index, "after.txt") #Sample quotes found
        quotebank.write_matching_quotes_to_file_for_year(index)
        
        
        quotebank.delete_json_lines_for_all_keywords()


def quotation_classification_for_file(filename):
    """
    For every line of the input file (json file), extract the quotation.
    If any of the keyword is found inside the quotation, the corresponding (json) line gets saved inside json_lines attribute of the corresponding
    keyword object.
    :param filename: str 
    """
    if not os.path.isfile(filename):
        print(filename + " doesn't exist")
        return

    with bz2.open(filename, "rb") as file:
        for i, line in tqdm(enumerate(file)):
            if i ==100000: break
            quotation = utils.extract_quotation(line)
            found_keywords = quotebank.match_quotation_with_any_keyword(quotation)
            if len(found_keywords) > 0:
                # Add country of speaker to line
                line = country_utils.expand_line(line, SPEAKER_ATTRIBUTES)
                for found_keyword in found_keywords:
                    found_keyword.json_lines.append(line)


# START
#syn_utils.add_new_synonyms(KEYWORDS_FILE_PATH, KEYWORDS_JSON_FILE_PATH)
SPEAKER_ATTRIBUTES = pd.read_parquet("data/speaker_attributes.parquet")

quotebank = QuoteBankData("Asymmetry of News", [])
quotebank.read_keywords_from_file()
utils.create_directories_for_every_year()
quotebank.create_json_dumps_filenames_for_each_keyword()
quotation_classification()

# Filter some topics
#filter_quotes_with_BERT(path, TOPICS_FOR_CLUSTERING)





