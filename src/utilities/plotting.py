import matplotlib.pyplot as plt
import random
from src.CONSTS import COLORS, DEATHS_INFO_COLUMNS
import numpy as np

def plot_line_chart(df, x_axis, y_axis, y_label, title, log_y = True, y_start_0 = False):
    """
    Plots line chart with logarithmic y-axis as standard. 
    Will extract 7 random elements from y_axis if len(y_axis) > 7.
    """
    ax = plt.gca()
    if len(y_axis) > 7:
        y_axis = random.sample(y_axis, 7)
    
    for i, col in enumerate(y_axis):
        df.plot(kind='line', x=x_axis, y=col, ax=ax, color=COLORS[i%len(COLORS)], logy=log_y, title=title, xlabel=x_axis, ylabel=y_label)
    
    if y_start_0:
        if log_y:
            ax.set_ylim(ymin=1)
        else:
            ax.set_ylim(ymin=0) 
        
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel = x_axis
    plt.ylabel = y_label
    plt.title = title
    plt.show()
    

def plot_stacked_area_chart(df_original, x_axis, y_axis_original, y_label, title, percentage_treshold = 3):
    """
    Plots stacked area chart.
    """
    
    df = df_original.copy()
    y_axis = y_axis_original.copy()
    other = np.zeros(10)
    for column in df:
        if column in DEATHS_INFO_COLUMNS: continue
        if df[column].max() < percentage_treshold:
            other += df[column].values
            df.drop([column], axis=1, inplace=True)
            y_axis.remove(column)
    
    df = df[y_axis +[x_axis]]
    df = df.assign(Other=other)
    
    ax = df.plot.area(x=x_axis, title=title, xlabel=x_axis, ylabel=y_label)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlabel = x_axis
    plt.ylabel = y_label
    plt.title = title
    plt.show()
