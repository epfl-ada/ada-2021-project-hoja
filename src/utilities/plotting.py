import matplotlib.pyplot as plt
import random
from src.CONSTS import COLORS

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
    
    
def plot_stacked_area_chart(df, x_axis, y_axis, y_label, title):
    """
    Plots stacked area chart.
    """
    df = df[y_axis +[x_axis]]
    
    ax = df.plot.area(x=x_axis, title=title, xlabel=x_axis, ylabel=y_label)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.xlabel = x_axis
    plt.ylabel = y_label
    plt.title = title
    plt.show()
