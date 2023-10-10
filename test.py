"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import os

import numpy as np

# Number of cores/threads
n_threads = os.cpu_count()  # Number of cores/threads
test_threads = np.linspace(2, n_threads, 8, dtype=int)  # Number of threads to test

# Number of emails to test
test_sizes = np.linspace(1e4, 1e8, 50, dtype=int)  # Number of emails to test
# test_sizes = np.logspace(4, 7, 50, base=10, dtype=int)  # Number of emails to test

# Bloom Filter
fpr = 0.01  # False Positive Rate

# Results and dataset filenames
results_filename = 'results/results.csv'
bitarray_filename = 'results/bitarray.mmap'
plot_filename = 'results/plot.png'

plot_time_filename = 'results/plot_time.png'
plot_speedup_filename = 'results/plot_speedup.png'
plot_fpr_filename = 'results/plot_fpr.png'


# key value for the results dictionary
test_key = 'test'
time_seq_key = 'time_seq'
fpr_key = 'fpr'
time_par_key = 'time_par'
speedup_key = 'speedup'

