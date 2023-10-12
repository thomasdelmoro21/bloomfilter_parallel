"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import os

import numpy as np

# Number of cores/threads
n_threads = os.cpu_count()  # Number of cores/threads
test_threads = np.linspace(2, n_threads, 4, dtype=int)  # Number of threads to test

# Number of emails to test setup
test_sizes = np.linspace(1e4, 1e7, 5, dtype=int)  # Number of emails to test
# test_sizes = np.logspace(4, 7, 50, base=10, dtype=int)  # Number of emails to test

# Number of spam emails to test
spam_sizes = np.linspace(1e4, 1e7, 5, dtype=int)

# Bloom Filter
fpr = 0.01  # False Positive Rate

# Results and dataset filenames
setup_results_filename = 'results/results.csv'
filter_results_filename = 'results/filter.csv'
chunks_results_filename = 'results/chunks.csv'
bitarray_filename = 'results/bitarray.mmap'
plot_setup_filename = 'results/plot_setup.png'
plot_filter_filename = 'results/plot_filter.png'
plot_chunks_filename = 'results/plot_chucks.png'
plot_time_filename = 'results/plot_time.png'
plot_speedup_filename = 'results/plot_speedup.png'
plot_fpr_filename = 'results/plot_fpr.png'


# key value for the results dictionary
test_key = 'test'
time_seq_key = 'time_seq'
fpr_key = 'fpr'
time_par_key = 'time_par'
speedup_key = 'speedup'

