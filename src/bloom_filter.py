"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import math
import shutil
import tempfile
import time

import mmh3
import numpy as np
from joblib import Parallel, delayed

from test import bitarray_filename


class BloomFilter:
    def __init__(self, fpr):
        self.size = 0
        self.n_hashes = 0
        self.fpr = fpr
        self.bitarray = None

    def initialize(self, items):
        self.reset()
        n = len(items)
        self.size = math.ceil(-(n * math.log(self.fpr)) / (math.log(2) ** 2))
        self.n_hashes = math.ceil((self.size / n) * math.log(2))
        self.bitarray = np.memmap(bitarray_filename, dtype=bool, mode='w+', shape=(self.size,))
        self.bitarray[:] = False

    def seq_setup(self, items):
        self.initialize(items)
        # Start sequential setup
        start = time.time()
        self.add(items)
        return time.time() - start

    def par_setup(self, items, n_threads, chunks=None):
        self.initialize(items)
        # Split items in chunks
        chunks = np.array_split(items, chunks if chunks else n_threads)
        # Start parallel setup
        start = time.time()
        Parallel(n_jobs=n_threads)(delayed(self.add)(chunk) for chunk in chunks)
        return time.time() - start

    def add(self, items):
        for item in items:
            for i in range(self.n_hashes):
                index = mmh3.hash(item, i) % self.size
                self.bitarray[index] = True

    def seq_filter_all(self, items):
        errors = 0
        start = time.time()
        for item in items:
            if self.filter(item):
                errors += 1
        return time.time() - start, errors

    def par_filter_all(self, items, n_threads):
        # Split items in chunks
        chunks = np.array_split(items, n_threads)
        # Start parallel setup
        start = time.time()
        results = Parallel(n_jobs=n_threads)(delayed(self.seq_filter_all)(chunk) for chunk in chunks)
        end_time = time.time() - start
        t, errs = zip(*results)
        errors = sum(errs)
        return end_time, errors

    def filter(self, item):
        for i in range(self.n_hashes):
            index = mmh3.hash(item, i) % self.size
            if not self.bitarray[index]:
                return False
        return True

    def reset(self):
        self.size = 0
        self.n_hashes = 0
        self.bitarray = None
        try:
            shutil.rmtree(tempfile.mkdtemp())
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
