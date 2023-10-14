"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import os
import numpy as np

# Number of cores/threads
n_threads = os.cpu_count()

# Number of threads to test
test_threads = np.linspace(2, n_threads, int(n_threads/2), dtype=int)  # Number of threads to test

# Number of test
tests = 4

# Number of emails to test setup
test_sizes = np.linspace(1e4, 1e7, tests, dtype=int)  # Number of emails to test

# Number of spam emails to test
spam_sizes = np.linspace(1e4, 1e7, tests, dtype=int)

# Number of chunks to test
test_chunks = [n_threads * 2 ** i for i in range(7)]

# Bloom Filter
fpr = 0.01  # False Positive Rate

# Filenames
# Bitarray filename
bitarray_filename = 'results/bitarray.mmap'

# Results filenames
setup_results_filename = 'results/csv/setup.csv'
filter_results_filename = 'results/csv/filter.csv'
chunks_results_filename = 'results/csv/chunks.csv'

# Plots filenames
plot_setup_filename = 'results/plots/plot_setup.png'
plot_filter_filename = 'results/plots/plot_filter.png'
plot_chunks_filename = 'results/plots/plot_chunks.png'


# key value for the results dictionary
test_key = 'test'
time_seq_key = 'time_seq'
fpr_key = 'fpr'
time_par_key = 'time_par'
speedup_key = 'speedup'

