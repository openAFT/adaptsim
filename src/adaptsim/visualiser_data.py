import pandas as pd
from matplotlib import rcParams
import matplotlib.pyplot as plt
import seaborn as sns

def data_reader(filename, key_1, entry_1, key_2=False, entry_2=False, sep=',', plot_sets=None):
    if plot_sets:
        rcParams.update(plot_sets)
    df_load = pd.read_csv(filename, sep=sep)
    df = df_load.loc[(df_load['patient'] < 31)]
    if key_2 and entry_2:
        return df.loc[(df[key_1]==entry_1) & (df[key_2]==entry_2)]
    else:
        return df.loc[(df[key_1]==entry_1)]

def plot_single(data, x, y, hue, x_label=None, y_label=None, minor_ticks=True, palette='Set2', plot_sets=None):
    if plot_sets:
        rcParams.update(plot_sets)
    ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, palette=palette, alpha=.8)
    if not minor_ticks:
        ax.tick_params(axis='x', which='minor', bottom=False)
    fig = ax.get_figure()
    if x_label != None and y_label != None:
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    ax.legend_.set_title(hue)
    fig.subplots_adjust(left=0.18, bottom=0.2, right=0.93, top=0.95)
    return fig

def plot_grid(data, x, y, hue, row, x_label=None, y_label=None, palette='Set2', plot_sets=None):
    if plot_sets:
        rcParams.update(plot_sets)
        [length, height] = plot_sets["figure.figsize"]
        aspect = length/height

    fig = sns.FacetGrid(data=data, hue=hue, row=row, height=height, aspect=aspect, palette=palette)
    fig.map(sns.scatterplot, x, y, alpha=.8)
    fig.despine(top=False, right=False)
    fig.add_legend()
    fig.legend.set_title(hue)
    if x_label != None and y_label != None:
        fig.set_axis_labels(x_label, y_label)
    fig.set_titles(row_template=row+": "+"{row_name}")
    fig.tight_layout(w_pad=1)
    return fig

def plot_single_fraction(data, x, y, hue, x_label, y_label, y_twin_label, y_twin=None, palette='Set2', plot_sets=None):
    if plot_sets:
        rcParams.update(plot_sets)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=data, x=x, y=y, hue=hue, palette=palette, marker='^')
    if y_twin != None:
        ax2 = ax.twinx()
        sns.lineplot(data=data, x=x, y=y_twin, hue=hue, palette=palette, linestyle='-')
        ax2.get_legend().remove()
        ax2.invert_yaxis()
        ax2.set_ylabel(y_twin)
        ax2.set_ylabel(y_twin_label)
    ax.set(xlabel=x_label, ylabel=y_label)
    ax.legend_.set_title(hue)
    return fig

def plot_twin_grid(data, x, y, y_twin, hue, row, x_label=None, y_label=None, y_twin_label=None, palette='Set2', plot_sets=None):
    if plot_sets:
        rcParams.update(plot_sets)
        [length, height] = plot_sets["figure.figsize"]
        aspect = length/height
    unique_palette = sns.color_palette(palette, n_colors=len(data[hue].unique()))
    palette_dict = dict(zip(data[hue].unique(), unique_palette))

    fig = sns.relplot(data=data, x=x, y=y, hue=hue, row=row, palette=palette_dict, style=hue, markers=['^'], height=height, aspect=aspect)
    for index, [oar, ax] in enumerate(fig.axes_dict.items()):
        ax2 = ax.twinx()
        data_sub = data.loc[data[row]==oar]
        sns.lineplot(data=data_sub, x=x, y=y_twin, hue=hue, palette=palette_dict, linestyle='-')
        ax2.get_legend().remove()
        ax2.invert_yaxis()
        ax2.set_ylabel(y_twin_label)
    fig.set_axis_labels(x_label, y_label)
    fig.legend.set_title(hue)
    fig.set_titles(row_template=row+": "+"{row_name}")
    fig.tick_params(axis='x', which='minor', bottom=False)
    fig.tight_layout(w_pad=1)
    return fig