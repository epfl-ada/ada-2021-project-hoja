"""
File name: Deaths.py
Author: HOJA
Date created: 1/11/2021
Date last modified: 12/11/2021
Python Version: 3.8
"""


import pandas as pd


class Deaths:

    def __init__(self, name, columns, static_columns):
        self.name = name
        self.deaths = pd.DataFrame(
            columns=columns)
        self.deaths_percentage = ""
        self.death_columns = columns.remove(static_columns)

    def plot_all_death_cols(self):
        for col in self.death_columns:
            continue
            