"""
File name: deaths_df_utils.py
Author: HOJA
Date created: 06/12/2021
Date last modified: 06/12/2021
Python Version: 3.8
"""

from sklearn.linear_model import LinearRegression
import numpy as np
from src.CONSTS import *
import math
import matplotlib.pyplot as plt


def modify_cols(df, rename_cols = {}, drop_cols=[]):
    """
    Renames and drops columns, and drops all rows with Year < 2007.
    """
    df = df[df["Year"] > 2007]
    df = df.drop(drop_cols, axis=1)
    cols = list(df.columns)
    for i, col in enumerate(cols):
        if (len(col.split(" - ")) > 1) and (col not in rename_cols.keys()):
            rename_cols[col] = col.split(" - ")[1].strip().replace(" ", "_")
    df = df.rename(columns=rename_cols)
    df = df.reset_index(drop=True)
    return df


def combine_cols(df):
    """
    Renames and drops columns, and drops all rows with Year < 2007.
    """
    for new_col_name, old_col_names in COMBINED_COLS.items():
        summed = df[old_col_names[0]]
        df = df.drop(old_col_names[0], axis=1)
        for i in range(1, len(old_col_names)):
            summed += df[old_col_names[i]]
            df = df.drop(old_col_names[i], axis=1)
        df[new_col_name] = summed
    return df


def extract_world_data(df):
    """
    Drop all rows where Entity != World.
    """
    df = df[df["Entity"] == "World"]
    df = df.reset_index(drop=True)
    return df


def update_nan_values(df, quant_columns):
    """
    Use linear regression based on the values from the other years to predict a value for all NaN cells.
    """
    for col in quant_columns:
        train_data = []
        pred_years = []
        for year in range(BEGIN_YEAR, END_YEAR + 1):
            val = df.loc[df['Year'] == year, col].iloc[0]
            if math.isnan(val):
                pred_years.append(year)
            else: train_data.append([year, val])
        
        if (len(pred_years) == 0): continue
        
        X = np.array(train_data)[:,0].reshape(-1,1)
        y = np.array(train_data)[:,1].reshape(-1,1)
        
        pred_years, predicted_values, regsr = predict_col_nan_values(X, y, pred_years)
        plot_predicted_values(X, y, pred_years, predicted_values, regsr, col)
        df = update_col_nan_values(df, pred_years, predicted_values, col)

    return df


def predict_col_nan_values(X, y, pred_years):
    """
    Predicts col nan values with linear regression.
    """
        
    pred_years = np.array(pred_years).reshape(-1,1)
    predicted_values, regsr = pred_with_linear_regression(X, y, pred_years)
    
    return pred_years, predicted_values,regsr


def pred_with_linear_regression(X, y, pred):
    """
    General linear regression model and prediction.
    """
    regsr = LinearRegression()
    regsr.fit(X,y)
    return regsr.predict(pred), regsr


def update_col_nan_values(df, x, y, col):
    """
    Replace nan values with predicted values for a column.
    """
    for i, val in enumerate(y):
        df.loc[df['Year'] == x[i][0], col] = y[i][0]
    return df


def plot_predicted_values(X, y, to_predict_x, predicted_y, regsr, col):
    """
    Plot predicted values in green, trend line in red and training values in blue.
    """
    
    m = regsr.coef_
    c = regsr.intercept_

    plt.title('Predicted death tolls for ' + str(col))  
    plt.xlabel('Year')
    plt.ylabel('Deaths') 

    plt.scatter(X,y,color="blue")

    new_y = [m*i+c for i in np.append(X, to_predict_x)]
    new_y = np.array(new_y).reshape(-1,1)

    plt.scatter(X,y,color="blue")
    plt.scatter(to_predict_x, predicted_y, color="green")
    plt.plot(np.append(X,to_predict_x),new_y,color="red")

    plt.show()
