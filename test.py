"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import os
import numpy as np

# Number of cores/threads
n_threads = os.cpu_count()

# Test
test_threads = np.linspace(2, n_threads, int(n_threads/2), dtype=int)  # Number of threads to test
tests = 10
test_sizes = np.linspace(1e4, 1e7, tests, dtype=int)  # Number of emails to test setup
spam_sizes = np.linspace(1e4, 1e7, tests, dtype=int)  # Number of spam emails to test
test_chunks = [(n_threads * 2 ** i) for i in range(8)]  # Number of chunks to test

# Bloom Filter
fpr = 0.01  # False Positive Rate
test_spam_fpr = 1000  # Number of spam emails to test FPR

# Filenames
bitarray_filename = 'results/bitarray.mmap'
emails_filename = 'dataset/emails.pkl'
spams_filename = 'dataset/spams.pkl'

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

