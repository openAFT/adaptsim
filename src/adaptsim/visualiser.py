# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import Normalize as normalise
import matplotlib.cm as cm
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
        marker='^', color='black')
    ax2.invert_yaxis()
    ax2.set_ylabel(r'$\delta$')
    # ax.legend(title='sf')
    ax.set_ylabel(r'BED$_{10}$')
    ax.set_xlabel(r'Fraction $t$')
    ax.set_xticks(range(min(x), max(x)+1))
    ax.tick_params(axis='x', which='minor', bottom=False)
    lines, labels = ax.get_legend_handles_labels()
    cross, clabels = ax2.get_legend_handles_labels()
    ax2.legend(lines + cross, labels + clabels, loc=1)
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

def plot_val_single(sfs, states, data, fractions, index, label, colmap='turbo', plot_sets=afs.RCPARAMS):
    rcParams.update(plot_sets)
    [n_grids, _, _] = data.shape
    # search for optimal rectangular size of subplot grid
    n_rows = n_columns = int(np.sqrt(n_grids))
    while n_rows * n_columns < n_grids:
        if n_rows >= n_columns:
            n_columns += 1
        else:
            n_rows += 1
    # initiate plot and parameters
    fig, ax = plt.subplots(1, 1)
    x_min, x_max, y_min, y_max = sfs[0], sfs[-1], states[0], states[-1]

    # create shared colorbar
    colmin, colmax = np.min(data), np.max(data)
    normaliser = normalise(colmin, colmax)
    colormap = cm.get_cmap(colmap)
    im = cm.ScalarMappable(cmap=colormap, norm=normaliser)

    # loop through the axes
    try:
        axs = ax.ravel()
    except:
        # in case ax is a 1x1 subplot
        axs = np.array([ax])

    i = np.where(fractions==index)[0][0]
    axs[0].imshow(data[i], interpolation=None, origin='upper',
        norm=normaliser, cmap=colormap, aspect='auto',
        extent=[x_min, x_max, y_min, y_max])
    axs[0].set_title(rf'${fractions[i]}$', loc='left')
    axs[0].set_xlabel(r'$\delta$')
    axs[0].set_ylabel(r'$B^{T}$')

    fig.tight_layout()
    fig.colorbar(mappable=im, ax=axs.tolist(), label=label)

    return fig

def plot_val_all(sfs, states, data_full, fractions, label, colmap='turbo', plot_sets=afs.RCPARAMS):
    data = data_full[:-1]
    rcParams.update(plot_sets)
    [n_grids, _, _] = data.shape
    # search for optimal rectangular size of subplot grid
    n_rows = n_columns = int(np.sqrt(n_grids))
    while n_rows * n_columns < n_grids:
        if n_rows >= n_columns:
            n_columns += 1
        else:
            n_rows += 1
    # initiate plot and parameters
    fig, ax = plt.subplots(n_rows, n_columns)
    x_min, x_max, y_min, y_max = sfs[0], sfs[-1], states[0], states[-1]

    # create shared colorbar
    colmin, colmax = np.min(data_full), np.max(data_full)
    normaliser = normalise(colmin, colmax)
    colormap = cm.get_cmap(colmap)
    im = cm.ScalarMappable(cmap=colormap, norm=normaliser)

    # loop through the axes
    try:
        axs = ax.ravel()
    except:
        # in case ax is a 1x1 subplot
        axs = np.array([ax])

    # turn off axes
    for a in axs:
        a.axis(False)

    for i, pol in enumerate(data):
        axs[i].axis(True)
        axs[i].imshow(pol, interpolation=None, origin='upper',
            norm=normaliser, cmap=colormap, aspect='auto',
            extent=[x_min, x_max, y_min, y_max])
        axs[i].set_title(fractions[i], loc='left')
        try: # get rid of inner axes values
            axs[i].label_outer()
        except:
            pass

    fig.supxlabel(r'$\delta$')
    fig.supylabel(r'$B^{T}$')

    # fig.tight_layout()
    fig.subplots_adjust(wspace=0.3, hspace=0.3, bottom=0.13, right=0.98)
    fig.colorbar(mappable=im, ax=axs.tolist(), label=label)

    return fig

def save_plot(fig, filename):
    basename = filename.rsplit('.')[0]
    fig.savefig(f'{basename}.pdf', bbox_inches='tight', format='pdf')

def show_plot():
    plt.show()