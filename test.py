import os

test_sizes = [10**i for i in range(2, 7)]
n_threads = os.cpu_count()  # Number of cores/threads
test_threads = range(2, n_threads+1, 2)  # Number of threads to test
fpr = 0.01  # False Positive Rate
# filter_size = 8000000  # 8MB

