"""
File name: Deaths.py
Author: HOJA
Date created: 4/12/2021
Date last modified: 06/12/2021
Python Version: 3.8
"""


import pandas as pd
from src.utilities.death_df_utils import *
from src.CONSTS import DEATHS_INFO_COLUMNS
from src.utilities.plotting import *
from src.utilities.utils import *


class Deaths:

    def __init__(self, name, path, rename_cols = {}, drop_cols = []):
        self.name = name
        self.columns = []
        self.quant_columns = []
        self.df = self.modify_df(pd.read_csv(path), rename_cols, drop_cols)
        self.percentage_df = percentage_of_total_count(self.df, self.quant_columns)
    
    def modify_df(self, df, rename_cols, drop_cols):

        df = modify_cols(df, rename_cols, drop_cols)
        df = update_col_names(df)
        if self.name == "deaths_by_cause":
            df = combine_cols(df)
        self.columns = df.columns
        self.quant_columns =  [col for col in self.columns if col not in DEATHS_INFO_COLUMNS]
        df = extract_world_data(df)
        
        df = update_nan_values(df, self.quant_columns)
        
        return df
    

    def plot_lines(self, y_label, title):
        plot_line_chart(self.df, "Year", self.quant_columns, y_label, title)
    
    def plot_stacked_areas(self, y_label, title):
        plot_stacked_area_chart(self.percentage_df, "Year", self.quant_columns, y_label, title)
      