from matplotlib import cycler, font_manager

ALL_SIM_DICT = {'n_patients': None,
                'fixed_mean_sample': None,
                'fixed_std_sample': None,
                'c_list': None,
                'plot_index': 1,
                'figsize': (6,4),
                'fontsize': 14,
                'save': 0,
                'use_tex': 0
                }

KEY_DICT_SIM = {'sim': list(ALL_SIM_DICT)}

plot_color_cycle = cycler('color', ['000000', '0000FE', 'FE0000', '008001', 'FD8000','8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf'])
plot_line_cycle = cycler('linestyle', ['-', '--', ':', '-.'])

RCPARAMS = {"figure.figsize": (6,4),
            "font.size": 14,
            "text.usetex": False,
            "axes.labelpad": 10,
            "axes.linewidth": 1.1,
            "axes.xmargin": 0.05,
            "axes.xmargin": 0.05,
            "axes.prop_cycle": plot_line_cycle,
            "axes.autolimit_mode"  : "data",
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
            "lines.markersize"     : 9,
            "lines.markerfacecolor" : "none",
            "lines.markeredgewidth"  : 0.8}

# if "CMU Sans Serif" in font_manager.get_font_names():
#     RCPARAMS["font.family"] = "sans-serif"
#     RCPARAMS["font.sans-serif"] = "CMU Sans Serif"