import numpy as np
import matplotlib.pyplot as plt
from adaptfx import multiple
from matplotlib import rcParams, cycler
from matplotlib.ticker import AutoMinorLocator

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.size'] = 16
rcParams['axes.linewidth'] = 1.1
rcParams['axes.labelpad'] = 10.0
plot_color_cycle = cycler('color', ['000000', '0000FE', 'FE0000', '008001', 'FD8000', '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf'])
rcParams['axes.prop_cycle'] = plot_color_cycle
rcParams['axes.xmargin'] = 0
rcParams['axes.ymargin'] = 0
rcParams.update({"axes.autolimit_mode" : "round_numbers",
                 "xtick.major.size"     : 7,
                 "xtick.minor.size"     : 3.5,
                 "xtick.major.width"    : 1.1,
                 "xtick.minor.width"    : 1.1,
                 "xtick.major.pad"      : 5,
                 "xtick.minor.visible" : True,
                 "ytick.major.size"     : 7,
                 "ytick.minor.size"     : 3.5,
                 "ytick.major.width"    : 1.1,
                 "ytick.minor.width"    : 1.1,
                 "ytick.major.pad"      : 5,
                 "ytick.minor.visible" : True,
                 "lines.markersize" : 10,
                 "lines.markerfacecolor" : "none",
                 "lines.markeredgewidth"  : 0.8})

#-------------------------------------------------------------------
typ = 1
n_frac = 7
ex = 2
sf = 1
sf_array = np.ones(n_frac+1) * sf
sf_array[ex] = 1.1
mu = 1
sigma = 0.08
c_list = np.linspace(0, 12, 5)
c_single = 0.5
#-------------------------------------------------------------------
inter_fraction = 0

def plot_fraction(fig, ax, dose_array, n_frac, sf, mu, std, const):
    x = np.arange(1, n_frac+1)
    y = dose_array
    ax.plot(x,y, label=const, linestyle='-', alpha=0.5)
    ax.set_title(f'mu={mu}, std={std}, sf={sf}')
    ax.set_ylabel('dose')
    ax.set_xlabel('fraction')
    ax.set_xticks(range(min(x), max(x)+1))
    ax.tick_params(axis='x', which='minor', bottom=False)
    fig.legend(title='C')

def check_skips(dose, n):
    if dose[n-1] != 0 and dose[n]== 0:
        print('no skip')
    else:
        print('skipped all')

#-------------------------------------------------------------------

if typ==1:

    fig, ax = plt.subplots(1,1, figsize=(6,4))
    dose_delivery = np.zeros((len(c_list),n_frac))

    for i, c in enumerate(c_list):
        frac_keys = {
            "number_of_fractions": n_frac,
            "fraction": 0,
            "sparing_factors": sf_array,
            "fixed_prob": 1,
            "fixed_mean": mu,
            "fixed_std": sigma,
            "min_dose": 0,
            "max_dose": -1,
            "tumor_goal": 72,
            "c": c,
            'abt': 10,
            'abn': 3,
            'accumulated_oar_dose': 0,
            'accumulated_tumor_dose': 0,
            }
        output = multiple('frac', frac_keys)
        tumor_dose = output.tumor_doses
        print(output.tumor_sum, output.oar_sum)
        plot_fraction(fig, ax, tumor_dose, n_frac, sf_array, mu, sigma, c)

#------------------------------------------------------------
plt.tight_layout()
plt.show()
