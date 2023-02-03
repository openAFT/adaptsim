# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize as normalise
import matplotlib.cm as cm
from matplotlib import rcParams, cycler

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['axes.linewidth'] = 1.1
rcParams['axes.labelpad'] = 10.0
plot_color_cycle = cycler('color', ['000000', '0000FE', 'FE0000', '008001', 'FD8000','8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf'])
plot_line_cycle = cycler('linestyle', ['-', '--', ':', '-.'])
rcParams['axes.prop_cycle'] = plot_line_cycle
rcParams['axes.xmargin'] = 0.05
rcParams['axes.ymargin'] = 0.05
rcParams.update({"axes.autolimit_mode"  : "data",
                 "xtick.major.size"     : 7,
                 "xtick.minor.size"     : 3.5,
                 "xtick.major.width"    : 1.1,
                 "xtick.minor.width"    : 1.1,
                 "xtick.major.pad"      : 5,
                 "xtick.minor.visible"  : True,
                 "ytick.major.size"     : 7,
                 "ytick.minor.size"     : 3.5,
                 "ytick.major.width"    : 1.1,
                 "ytick.minor.width"    : 1.1,
                 "ytick.major.pad"      : 5,
                 "ytick.minor.visible"  : True,
                 "lines.markersize"     : 7,
                 "lines.markerfacecolor" : "none",
                 "lines.markeredgewidth"  : 0.8})

def plot_dose(data, sf_list, n_frac, c_list):
    """
    creates a plot of applied dose and corresponding sparing factor

    Parameters
    ----------
    data : array
        2d array
    sf_list : array
        1d array with dimension n
    n_frac : int

    Returns
    -------
    ax : matplotlib.pyplot.axes

    """
    x = np.arange(1, n_frac+1)
    fig, ax = plt.subplots(1,1, figsize=(6,4))
    for i, c in enumerate(c_list):
        ax.plot(x, data[i], label=f'c={c}', alpha=0.5, color='black')
    ax2 = ax.twinx()
    ax2.scatter(x, sf_list[1:], label=r'$\delta$',
        marker='1', color='black')
    ax2.invert_yaxis()
    ax2.set_ylabel('sparing factor')
    # ax.legend(title='sf')
    ax.set_ylabel('dose')
    ax.set_xlabel('fraction')
    ax.set_xticks(range(min(x), max(x)+1))
    ax.tick_params(axis='x', which='minor', bottom=False)
    lines, labels = ax.get_legend_handles_labels()
    cross, clabels = ax2.get_legend_handles_labels()
    ax2.legend(lines + cross, labels + clabels, loc=0)
    fig.tight_layout()

    return ax

def plot_hist(data, n_frac):
    """
    creates a histogram plot of numbers of fractions used

    Parameters
    ----------
    data : array
        1d array
    n_frac : int

    Returns
    -------
    ax : matplotlib.pyplot.axes

    """
    x = np.arange(1, n_frac+1)
    fig, ax = plt.subplots(1,1, figsize=(6,4))
    ax.hist(data, bins=x, alpha=0.4, align= 'left',
        histtype= 'stepfilled', color='red')
    ax.set_xticks(range(min(x), max(x)+2))
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_ylabel('number of patients')
    ax.set_xlabel('fraction')
    fig.tight_layout()

    return ax

def show_plot():
    plt.show()