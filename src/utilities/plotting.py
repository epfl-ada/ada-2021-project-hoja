import matplotlib.pyplot as plt
import random
from src.CONSTS import *
import numpy as np
import pandas as pd


def plot_line_chart(df, x_axis, y_axis, y_label, title, log_y = True, y_start_0 = False):
    """
    Plots line chart with logarithmic y-axis as standard. 
    Will extract 7 random elements from y_axis if len(y_axis) > 7.
    """
    ax = plt.gca()
    if len(y_axis) > 7:
        y_axis = random.sample(y_axis, 7)
    
    for i, col in enumerate(y_axis):
        df.plot(kind='line', x=x_axis, y=col, ax=ax, colormap=COLOR_MAP, logy=log_y, title=title, xlabel=x_axis, ylabel=y_label)
    
    if y_start_0:
        if log_y:
            ax.set_ylim(ymin=1)
        else:
            ax.set_ylim(ymin=0) 
        
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel = x_axis
    plt.ylabel = y_label
    plt.title = title
    save_plt(title)
    plt.show()
    

def plot_stacked_area_chart(df_original, x_axis, y_axis_original, y_label, title, percentage_treshold = 3):
    """
    Plots stacked area chart.
    """
    
    df = df_original.copy()
    y_axis = y_axis_original.copy()
    
    other = np.zeros(df.shape[0])
    
    for column in df:
        if column in DEATHS_INFO_COLUMNS: continue
        if df[column].max() < percentage_treshold:
            other += df[column].values
            df.drop([column], axis=1, inplace=True)
            y_axis.remove(column)
    
    df = df[y_axis +[x_axis]]
    
    if (other!=np.zeros(df.shape[0])).all():
        df = df.assign(Other=other)
    
    ax = df.plot.area(x=x_axis, title=title, xlabel=x_axis, ylabel=y_label, colormap = COLOR_MAP)
    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlabel = x_axis
    plt.ylabel = y_label
    plt.title = title
    save_plt(title)
    plt.show()


def cause_pie_chart_plot(df, year, threshold, name):
    
    pc_df = df[TOPICS]
    pc_df = pc_df.iloc[[year - 2008]]
    
    other = 0
    sorted_pd = pd.DataFrame(np.sort(pc_df.values))
   
    for column in pc_df:
        if column in DEATHS_INFO_COLUMNS: continue
        if ((pc_df[column].values)) < sorted_pd.iloc[: ,-threshold].values:
            other += pc_df[column].values
            pc_df.drop([column], axis=1, inplace=True)
            
    pc_df = pc_df.assign(Other=other)
    pc_df.T.plot.pie(colormap=COLOR_MAP,subplots=True, figsize=(12, 8), legend=None, ylabel = ' ', autopct='%1.1f%%', pctdistance=0.7)
    plt.savefig('./generated/images/pie_chart_quotes_' + name + str(year) + '.png') 
    plt.show() 
    
def stacked_barplot(df, x_labels=None, y_label=None, title=None, width = 0.35, safe_name=None, log_y=False):
    columns = df.columns
    fig, ax = plt.subplots()
    df.plot.bar(colormap = COLOR_MAP, ax=ax, stacked = True, logy = log_y)

    ax.set_ylabel(y_label)
    ax.set_title(title)
    handles, lables_legend = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], lables_legend[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    
    if safe_name:
        save_plt(safe_name)
    
def save_plt(name):
    plt.savefig(GENERATED_IMAGES_PATH + name + '.png', bbox_inches = 'tight') 


