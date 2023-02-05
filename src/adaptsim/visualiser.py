# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import adaptsim as afs

def plot_dose(data, sf_list, n_frac, c_list, plot_sets=afs.RCPARAMS):
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
    rcParams.update(plot_sets)

    x = np.arange(1, n_frac+1)
    fig, ax = plt.subplots(1,1)
    for i, c in enumerate(c_list):
        ax.plot(x, data[i], label=rf'$C={c}$', alpha=0.5, color='black')
    ax2 = ax.twinx()
    ax2.scatter(x, sf_list[1:], label=r'$\delta_t$',
        marker='1', color='black')
    ax2.invert_yaxis()
    ax2.set_ylabel(r'$\delta$')
    # ax.legend(title='sf')
    ax.set_ylabel(r'BED$_3$')
    ax.set_xlabel(r'Fraction $t$')
    ax.set_xticks(range(min(x), max(x)+1))
    ax.tick_params(axis='x', which='minor', bottom=False)
    lines, labels = ax.get_legend_handles_labels()
    cross, clabels = ax2.get_legend_handles_labels()
    ax2.legend(lines + cross, labels + clabels, loc=0)
    fig.tight_layout()

    return fig

def plot_hist(data, n_frac, plot_sets=afs.RCPARAMS):
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
    rcParams.update(plot_sets)
    
    x = np.arange(1, n_frac+1)
    fig, ax = plt.subplots(1,1)
    ax.hist(data, bins=x, alpha=0.4, align= 'left',
        histtype= 'stepfilled', color='red')
    ax.set_xticks(range(min(x), max(x)+2))
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_ylabel(r'Number of Patients')
    ax.set_xlabel(r'Fraction $t$')
    fig.tight_layout()

    return fig

def save_plot(fig, filename):
    basename = filename.rsplit('.')[0]
    fig.savefig(f'{basename}.pdf', bbox_inches='tight', format='pdf')

def show_plot():
    plt.show()