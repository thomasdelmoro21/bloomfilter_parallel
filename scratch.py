import math
import time

import mmh3
import numpy as np
from joblib import delayed, Parallel

from generate_emails import *


def seq():
    # Start sequential setup
    start = time.time()
    for email in emails:
        add_seq(email)
    return time.time() - start


def par_setup(n_threads):
    # Start parallel setup
    start = time.time()
    Parallel(n_jobs=n_threads)(delayed(add_par)(emails) for emails in emails_chunk)
    return time.time() - start


def add_seq(item):
    for i in range(num_hashes):
        index = mmh3.hash(item, i) % dim
        bitarray_seq[index] = 1


def add_par(items):
    for email in items:
        for i in range(num_hashes):
            index = mmh3.hash(email, i) % dim
            bitarray_par[index] = 1


fpr = 0.01
n_email = 100000000
dim = math.ceil(-(n_email * math.log(fpr)) / (math.log(2) ** 2))
# dim = 10**8 max size of array

num_hashes = math.ceil((dim / n_email) * math.log(2))
bitarray_seq = [0] * dim
bitarray_par = np.memmap('bitarray.mmap', dtype=bool, mode='w+', shape=(dim,))
emails = [generation_email() for _ in range(n_email)]
emails_chunk = np.array_split(emails, 16)

# Start sequential setup
print("Sequential setup")
print(seq())

# Start parallel setup
print("Parallel setup")
print(par_setup(-1))
