# -*- coding: utf-8 -*-
import argparse
import json
import adaptfx as afx
import adaptsim as afs
import numpy as np
import sys
nme = __name__

class MC_object():
    """
    Reinforcement Learning class to check instructions
    of calculation, invoke keys and define
    calculation settings from file
    """
    def __init__(self, model_filename):
        model = afx.RL_object(model_filename)

        try: # check if file can be opened
            with open(model_filename, 'r') as f:
                read_in = f.read()
            raw_simulation_dict = json.loads(read_in)
        except TypeError:
            if isinstance(model_filename, dict):
                raw_simulation_dict = model_filename
            else:
                afx.aft_error(f'"{model_filename}" not a filename or dict', nme)
        except SyntaxError as syntax_err:
            afx.aft_error(f'error in "{model_filename}", {syntax_err}', nme)
        except OSError:
            afx.aft_error(f'No such file: "{model_filename}"', nme)
        except ValueError as decode_err:
            afx.aft_error(f'decode error in "{model_filename}", {decode_err}', nme)
        except:
            afx.aft_error(f'error in "{model_filename}", {sys.exc_info()}', nme)

        try:
            algorithm_simulation = raw_simulation_dict['algorithm_simulation']
        except KeyError as algo_err:
            afx.aft_error(f'{algo_err} key missing in: "{model_filename}"', nme)
        else:
            afx.aft_message_info('algorithm simulation:', algorithm_simulation, nme, 1)

        try: # check if simulation_keys exists and is a dictionnary
            raw_keys = raw_simulation_dict['keys_simulation']
        except KeyError:
            afx.aft_error(f'"keys_simulation" is missing in : "{model_filename}"', nme)
        else:
            simulation_dict = afx.key_reader(afs.KEY_DICT_SIM, afs.ALL_SIM_DICT, raw_keys, 'sim')
            afx.aft_message_dict('simulation', simulation_dict, nme)

        self.algorithm = model.algorithm
        self.log = model.log
        self.log_level = model.log_level
        self.keys_model = model.keys
        self.settings = model.settings
        self.algorithm_simulation = algorithm_simulation
        self.keys_simulation = afx.DotDict(simulation_dict)
        self.simulation_filename = model_filename


    def simulate(self):
        plot_sets = afs. RCPARAMS
        plot_sets["text.usetex"] = self.keys_simulation.usetex
        plot_sets["figure.figsize"] = self.keys_simulation.figsize
        plot_sets["font.size"] = self.keys_simulation.fontsize
        n_frac = self.keys_model.number_of_fractions
        if self.algorithm_simulation == 'histogram':
            n_patients = self.keys_simulation.n_patients 
            mu = self.keys_simulation.fixed_mean_sample
            std = self.keys_simulation.fixed_std_sample
            plans = np.zeros(n_patients)
            for i in range(n_patients):
                self.keys_model.sparing_factors = list(np.random.normal(mu , std, n_frac + 1))
                output = afx.multiple(self.algorithm, self.keys_model, self.settings)
                # output.oar_sum output.tumor_sum
                n_frac_used = np.count_nonzero(~np.isnan(output.physical_doses))
                plans[i] = n_frac_used
            hist = afs.plot_hist(plans, n_frac, plot_sets)

            if self.keys_simulation.save:
                afs.save_plot(hist, self.simulation_filename)
            
        elif self.algorithm_simulation == 'fraction':
            c_list = self.keys_simulation.c_list
            sf_list = self.keys_model.sparing_factors
            c_dose_array = np.zeros((len(c_list), n_frac))
            for i, c in enumerate(self.keys_simulation.c_list):
                self.keys_model.c = c
                output = afx.multiple(self.algorithm, self.keys_model, self.settings)
                c_dose_array[i] = output.tumor_doses
            self.c_dose_list = c_dose_array
            fracs = afs.plot_dose(self.c_dose_list, sf_list, n_frac, c_list, plot_sets)

            if self.keys_simulation.save:
                afs.save_plot(fracs, self.simulation_filename)
            else:
                self.plot()

        elif self.algorithm_simulation == 'single_state':
            out = afx.multiple(self.algorithm, self.keys_model, self.settings)
            if self.settings.plot_policy:
                poli = afs.plot_val_single(out.policy.sf, out.policy.states, out.policy.val,
                out.policy.fractions, self.keys_simulation.plot_index, r'BED$_{10}$', 'turbo', plot_sets)
            if self.settings.plot_values:
                poli = afs.plot_val_single(out.value.sf, out.value.states, out.value.val,
                out.value.fractions, self.keys_simulation.plot_index, 'Value', 'viridis', plot_sets)
            if self.settings.plot_remains:
                poli = afs.plot_val_single(out.remains.sf, out.remains.states, out.remains.val,
                out.remains.fractions, self.keys_simulation.plot_index, 'Expected Remaining Number', 'plasma', plot_sets)

            if self.keys_simulation.save:
                afs.save_plot(poli, self.simulation_filename)
            else:
                self.plot()

        elif self.algorithm_simulation == 'all_state':
            out = afx.multiple(self.algorithm, self.keys_model, self.settings)
            if self.settings.plot_policy:
                poli = afs.plot_val_all(out.policy.sf, out.policy.states, out.policy.val,
                out.policy.fractions, r'BED$_{10}$', 'turbo', plot_sets)
            if self.settings.plot_values:
                poli = afs.plot_val_all(out.value.sf, out.value.states, out.value.val,
                out.value.fractions, 'Value', 'viridis', plot_sets)
            if self.settings.plot_remains:
                poli = afs.plot_val_all(out.remains.sf, out.remains.states, out.remains.val,
                out.remains.fractions, 'Expected Remaining Number', 'plasma', plot_sets)

            if self.keys_simulation.save:
                afs.save_plot(poli, self.simulation_filename)
            else:
                self.plot()
        
    def plot(self):
        afs.show_plot()

def main():
    """
    CLI interface to invoke the RL class
    """
    start = afx.timing()
    parser = argparse.ArgumentParser(
        description='Patient Monte Carlo Simulation to test adaptive fractionation'
    )
    parser.add_argument(
        '-f',
        '--filename',
        metavar='',
        help='input adaptive fractionation instruction filename',
        type=str
    )
    # In case there is no input show help
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    sim = MC_object(args.filename)

    afx.aft_message('start session...', nme, 1)
    sim.simulate()
    afx.timing(start)
    afx.aft_message('close session...', nme, 1)


if __name__ == '__main__':
    main()
