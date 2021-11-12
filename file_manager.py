import bz2

DATA_PATH = './some_relative_path'


def read_keywords():
    with bz2.open(DATA_PATH, "rb") as file:
        pass
        # READING THE FILE AND APPEND KEYWORDS TO THE TOPIC OBJECT
