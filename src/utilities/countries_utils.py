# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 21:43:40 2021

@author: jurri
"""
import numpy as np
import pandas as pd
import pygal
from pygal.style import Style
from pycountry_convert import country_name_to_country_alpha2
from src.CONSTS import GENERATED_IMAGES_PATH, ALL_COUNTRIES_CODE, TOPICS

def reduce_df(df_original, percentage_treshold, return_percentage = False):
    df = df_original.copy()
    df_percentage = df.copy()
    # Check if rows are percentages
    if int(df_percentage.iloc[0].sum()) != 100:
        for index, row in df_percentage.iterrows():
            df_percentage.iloc[index] = (row/row.sum()) * 100
        
    other = np.zeros(len(df))
    other_percentage = np.zeros(len(df))
    for column in df:
        if df_percentage[column].max() < percentage_treshold:
            other += df[column].values
            other_percentage += df_percentage[column].values
            df.drop([column], axis=1, inplace=True)
            df_percentage.drop([column], axis=1, inplace=True)
            
    df = df.assign(Other=other)
    df_percentage = df_percentage.assign(Other=other_percentage)

    if not return_percentage:
        return df
    else:
        return df_percentage
      
def get_country_a2_code(col):
    try:
        cn_a2_code =  country_name_to_country_alpha2(col)
    except:
        cn_a2_code = 'Unknown'  
    return cn_a2_code

def map_countries_according_to_mag_order(totals_per_country, year):
    """Creates a mapping dict for the occurences of quotes according to order of magintude.
    Out put is a list of dicts, with first dict for countries for which between 10^0 and 
    10^1 quotes were found, etc.
    param: totals_per_country: dict
            year: int
            
    return: mapping: list of dicts"""
    
    c_code = list()
    countries = totals_per_country.keys()
    quotes = list()
    for country_year in countries:
        if country_year[1] == year:
            quotes.append(totals_per_country[country_year])
            cn_a2_code = get_country_a2_code(country_year[0])
            c_code.append(cn_a2_code)
    
    all_countries_code = ALL_COUNTRIES_CODE.copy()
    mapping = [dict() for i in range(7)]
    for i, code in enumerate(c_code):
        s_code = code.lower()
        if s_code in all_countries_code:
            all_countries_code.remove(s_code)
        if s_code != 'unknown':
            quote_order = np.log(quotes[i])/np.log(10)
            if quote_order < 1:
                mapping[1][s_code] = 1
            elif quote_order < 2:
                mapping[2][s_code] = 1
            elif quote_order < 3:
                mapping[3][s_code] = 1
            elif quote_order < 4:
                mapping[4][s_code] = 1
            elif quote_order < 5:
                mapping[5][s_code] = 1
            elif quote_order < 6:
                mapping[6][s_code] = 1
    # No data countries
    for country in all_countries_code:
        mapping[0][country] = 1

    return mapping

def create_world_map(mapping, safe_name, year):
    custom_style = Style(colors=('#D3D3D3','#4FFFFF','#00C9E4','#0094C2','#006198','#003269','#000036'))

    # create a world map
    worldmap =  pygal.maps.world.World(style=custom_style, show_legend=False)


    # adding the countries
    worldmap.add("No Data", mapping[0])
    for i in range(1,len(mapping)):
        if mapping[i].keys():
            worldmap.add(str("{:0.0f}-{:0.0f}".format(i-1,i)), mapping[i])

    worldmap.render_to_file(GENERATED_IMAGES_PATH + safe_name + '.svg')
    

def get_data_for_one_year(deaths, year):
    """
    Creates a dataframe, where each row represents a region, which is and each column a deathcause.
    Data is taken from deaths, a dict where each keyword is a region, where the value is the data for all years.
    param: deaths: dict
           year: int
           
    return: deaths_year: pd.DataFrame
            deaths_year_percentage: pd.DataFrame (percentage values)
    """
    deaths_year = pd.DataFrame()
    regions = list()
    for region in deaths:
        regions.append(region)
        deaths_year = deaths_year.append(deaths[region][TOPICS][deaths[region]["Year"] == year])
    
    # Get relative values for each year by calculating percentage
    deaths_year = deaths_year.reset_index()
    deaths_year_percentage = deaths_year.copy()
    for i in range(len(deaths_year)):
        deaths_year_percentage.loc[i] = deaths_year_percentage.loc[i]/deaths_year_percentage.loc[i].sum()*100

    return deaths_year, deaths_year_percentage, regions