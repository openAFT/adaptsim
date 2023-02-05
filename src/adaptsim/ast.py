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
    def __init__(self, model_filename, simulation_filename):
        model = afx.RL_object(model_filename)

        try: # check if file can be opened
            with open(simulation_filename, 'r') as f:
                read_in = f.read()
            raw_simulation_dict = json.loads(read_in)
        except TypeError:
            if isinstance(simulation_filename, dict):
                raw_simulation_dict = simulation_filename
            else:
                afx.aft_error(f'"{simulation_filename}" not a filename or dict', nme)
        except SyntaxError as syntax_err:
            afx.aft_error(f'error in "{simulation_filename}", {syntax_err}', nme)
        except OSError:
            afx.aft_error(f'No such file: "{simulation_filename}"', nme)
        except ValueError as decode_err:
            afx.aft_error(f'decode error in "{simulation_filename}", {decode_err}', nme)
        except:
            afx.aft_error(f'error in "{simulation_filename}", {sys.exc_info()}', nme)

        try:
            algorithm_simulation = raw_simulation_dict['algorithm']
        except KeyError as algo_err:
            afx.aft_error(f'{algo_err} key missing in: "{simulation_filename}"', nme)
        else:
            afx.aft_message_info('algorithm simulation:', algorithm_simulation, nme, 1)

        try: # check if simulation_keys exists and is a dictionnary
            raw_keys = raw_simulation_dict['simulation_keys']
        except KeyError:
            afx.aft_error(f'"simulation_keys" is missing in : "{simulation_filename}"', nme)
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
        self.simulation_filename = simulation_filename


    def simulate(self):
        if self.algorithm_simulation == 'histogram':
            n_patients = self.keys_simulation.n_patients 
            mu = self.keys_simulation.fixed_mean_sample
            std = self.keys_simulation.fixed_std_sample
            n_frac = self.keys_model.number_of_fractions
            plans = np.zeros(n_patients)
            for i in range(n_patients):
                self.keys_model.sparing_factors = list(np.random.normal(mu , std, n_frac + 1))
                output = afx.multiple(self.algorithm, self.keys_model, self.settings)
                # output.oar_sum output.tumor_sum
                n_frac_used = np.count_nonzero(~np.isnan(output.physical_doses))
                plans[i] = n_frac_used
            hist = afs.plot_hist(plans, n_frac)
            
            if self.keys_simulation.plot_bool:
                afs.save_plot(hist, self.simulation_filename)
            
        elif self.algorithm_simulation == 'fraction':
            c_list = self.keys_simulation.c_list
            n_fractions = self.keys_model.number_of_fractions
            sf_list = self.keys_model.sparing_factors
            c_dose_array = np.zeros((len(c_list), n_fractions))
            for i, c in enumerate(self.keys_simulation.c_list):
                self.keys_model.c = c
                output = afx.multiple(self.algorithm, self.keys_model, self.settings)
                c_dose_array[i] = output.tumor_doses
            self.c_dose_list = c_dose_array
            fracs = afs.plot_dose(self.c_dose_list, sf_list, n_fractions, c_list)

            if self.keys_simulation.plot_bool:
                afs.save_plot(fracs, self.simulation_filename)
        
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
        '--fractionation',
        metavar='',
        help='input adaptive fractionation instruction filename',
        type=str
    )
    parser.add_argument(
        '-s',
        '--simulation',
        metavar='',
        help='input adaptive fractionation instruction filename',
        type=str
    )
    # In case there is no input show help
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    sim = MC_object(args.fractionation, args.simulation)

    sim.simulate()

    # afx.aft_message('start session...', nme, 1)
    # sim.simulate()
    # afx.timing(start)

    # # show retrospective dose prescribtion
    # afx.aft_message_list('physical dose:', plan.output.physical_doses, nme, 1)
    # afx.aft_message_list('tumor dose:', plan.output.tumor_doses, nme)
    # afx.aft_message_list('oar dose:', plan.output.oar_doses, nme)

    # # show accumulated dose
    # afx.aft_message_info('accumulated oar dose:', plan.output.oar_sum, nme, 1)
    # afx.aft_message_info('accumulated tumor dose:', plan.output.tumor_sum, nme)
    # sim.plot()
    # afx.aft_message('close session...', nme, 1)


if __name__ == '__main__':
    main()
