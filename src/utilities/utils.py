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
