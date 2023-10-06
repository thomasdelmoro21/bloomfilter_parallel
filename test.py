import os

import numpy as np

# Number of cores/threads
n_threads = os.cpu_count()  # Number of cores/threads
test_threads = np.linspace(2, n_threads, 4, dtype=int)  # Number of threads to test

# Number of emails to test
test_sizes = np.logspace(4, 8, 10, base=10, dtype=int)  # Number of emails to test

# Bloom Filter
fpr = 0.01  # False Positive Rate

