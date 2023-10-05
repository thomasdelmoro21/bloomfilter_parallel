"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import functools
import math
import os
import shutil
import tempfile
import time

import mmh3
import numpy as np
from bitarray import bitarray
from joblib import Parallel, delayed


class BloomFilter:

    def __init__(self, size):
        self.size = size
        self.array = bitarray(size)
        self.array.setall(0)
        self.num_hashes = 0
        self.hashes = []

    def init_hashes(self, emails):
        self.num_hashes = int((self.size / len(emails)) * math.log(2))
        self.hashes = self.set_hashes(self.num_hashes)

    def setup(self, emails):
        self.init_hashes(emails)
        start = time.time()
        for email in emails:
            self.set_email(email)
        return time.time() - start

    def parallel_setup(self, emails, n_threads):
        self.init_hashes(emails)
        start = time.time()
        Parallel(n_jobs=n_threads)(delayed(self.set_email)(email) for email in emails)
        return time.time() - start

    def set_email(self, email):
        for hashFun in self.hashes:
            self.array[hashFun(email) % len(self.array)] = 1

    def set_hashes(self, num_hashes):
        self.hashes = []
        for i in range(num_hashes):
            self.hashes.append(functools.partial(mmh3.hash, seed=i))
        return self.hashes

    def filter_all(self, emails):
        errors = 0
        for email in emails:
            if self.filter(email):
                # print("Email Passed")
                errors += 1
        return errors

    def filter(self, m):
        for hashFun in self.hashes:
            pos = hashFun(m) % len(self.array)
            if self.array[pos] == 0:
                return False
        return True

    def reset(self):
        self.array.setall(0)
        self.num_hashes = 0
        self.hashes = []


class BloomFilterOptimized:
    def __init__(self, fpr):
        self.size = 0
        self.num_hashes = 0
        self.fpr = fpr
        self.bit_array = np.arange(0)

    def initialize(self, items):
        n = len(items)
        self.size = math.ceil(-(n * math.log(self.fpr)) / (math.log(2) ** 2))
        self.num_hashes = math.ceil((self.size / n) * math.log(2))
        self.bit_array = np.memmap('bitarray.mmap', dtype=bool, mode='w+', shape=(self.size,))
        self.bit_array[:] = 0

    def seq_setup(self, items):
        self.reset()
        self.initialize(items)
        # Start sequential setup
        start = time.time()
        self.add(items)
        return time.time() - start

    def par_setup(self, items, n_threads):
        self.reset()
        self.initialize(items)
        # Split items in chunks
        chunks = np.array_split(items, n_threads)
        # Start parallel setup
        start = time.time()
        Parallel(n_jobs=n_threads)(delayed(self.add)(chunk) for chunk in chunks)
        return time.time() - start

    def add(self, items):
        for item in items:
            for i in range(self.num_hashes):
                index = mmh3.hash(item, i) % self.size
                self.bit_array[index] = True

    def filter(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if not self.bit_array[index]:
                return False
        return True

    def filter_all(self, items):
        errors = 0
        for item in items:
            if self.filter(item):
                errors += 1
        return errors

    def reset(self):
        self.size = 0
        self.bit_array = np.arange(0)
        self.num_hashes = 0
        try:
            shutil.rmtree(tempfile.mkdtemp())
        except OSError:
            pass

