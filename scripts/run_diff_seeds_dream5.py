"""
Python script for running Arboretum multiple times on the DREAM5 dataset,
initialized with a different random seed for each run.

The objective is to assess the stability of the inference quality of GRNBoost2
compared with GENIE3/Arboretum and the GENIE3 results as reported in the Dream5 paper.
"""

import pandas as pd
import time

from arboretum.algo import genie3, grnboost2
from arboretum.utils import load_tf_names

DEFAULT_N_RUNS = 100

wd = '../resources/dream5/'

net1_expression = wd + 'net1/net1_expression_data.tsv'
net3_expression = wd + 'net3/net3_expression_data.tsv'
net4_expression = wd + 'net4/net4_expression_data.tsv'

net1_tfs = wd + 'net1/net1_transcription_factors.tsv'
net3_tfs = wd + 'net3/net3_transcription_factors.tsv'
net4_tfs = wd + 'net4/net4_transcription_factors.tsv'

datasets = [('net1', net1_expression, net1_tfs),
            ('net3', net3_expression, net3_tfs),
            ('net4', net4_expression, net4_tfs)]

algo = 'grnboost2'
out_dir = '../output/dream5/{}/'.format(algo)

# seeds = [seed * 100 for seed in range(0, 100)]
seeds = [seed * 100 for seed in range(0, 1)]

# dry_run = True
dry_run = False


def run_algo(algo_name, seed_value):

    if algo_name == 'genie3':
        inf_algo = genie3
    elif algo_name == 'grnboost2':
        inf_algo = grnboost2
    else:
        raise ValueError('Houston, we have a problem between desk and chair.. ({})'.format(algo_name))

    for network_name, exp_path, tfs_path in datasets:
        start_time = time.time()

        print('inferring {0} with seed {1}'.format(network_name, seed))

        exp_matrix = pd.read_csv(exp_path, sep='\t')
        tf_names = load_tf_names(tfs_path)
        network_df = inf_algo(expression_data=exp_matrix,
                              tf_names=tf_names,
                              seed=seed_value)

        inf_time = time.time()
        delta_time = inf_time - start_time

        print('inferred {0} with seed {1} in {2} seconds'.format(network_name, seed, str(delta_time)))

        network_out_path = '{0}{1}.seed_{2}.csv'.format(out_dir, network_name, seed)

        network_df.to_csv(network_out_path, sep='\t')

        print('{0} with seed {1} written to {2}'.format(network_name, seed, network_out_path))


if __name__ == '__main__':

    for seed in seeds:
        print('running {0} with seed {1}'.format(algo, seed))

        if not dry_run:
            run_algo(algo, seed)
