"""
File name: utils.py
Author: HOJA
Date created: 11/12/2021
Date last modified: 11/12/2021
Python Version: 3.8
"""


def percentage_of_total_count(df, columns):
    """
    Modifies death columns to percentages of total deaths
    """
    df = df.copy()
    df["Total count"] = 0
    for column in columns:
        df["Total count"] += df[column]
    for column in columns:
        df[column] = (df[column]/df["Total count"])*100
    df = df.drop("Total count", axis=1)
    return df


def prettify_column(column):
    column = column.lower().replace("_", " ").capitalize()
    return column


def prettify_all_column(columns):
    new_cols = []
    for col in columns:
        new_cols.append(prettify_column(col))
    return new_cols


def update_col_names(df):
    old_columns = df.columns
    new_columns = prettify_all_column(old_columns)
    for i in range(len(old_columns)):
        df = df.rename(columns={old_columns[i]: new_columns[i]})
    return df
