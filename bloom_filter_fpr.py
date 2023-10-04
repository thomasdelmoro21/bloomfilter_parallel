"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import functools
import math
from bitarray import bitarray
import mmh3
from joblib import Parallel, delayed
import time


class BloomFilter:

    def __init__(self, fpr):
        self.size = 0
        self.num_hashes = 0
        self.fpr = fpr
        self.array = bitarray()
        self.hashes = []

    def initialize(self, emails):
        n = len(emails)
        self.size = math.ceil(-(n * math.log(self.fpr)) / (math.log(2) ** 2))
        self.num_hashes = math.ceil((self.size / n) * math.log(2))
        self.hashes = self.set_hashes(self.num_hashes)
        self.array = bitarray(self.size)
        self.array.setall(0)

    def setup(self, emails):
        self.initialize(emails)
        start = time.time()
        for email in emails:
            self.set_email(email)
        return time.time() - start

    def parallel_setup(self, emails, n_threads):
        self.initialize(emails)
        start = time.time()
        Parallel(n_jobs=n_threads)(delayed(self.set_email)(email)for email in emails)
        return time.time() - start

    def set_email(self, email):
        for hashFun in self.hashes:
            self.array[hashFun(email) % len(self.array)] = 1

    def set_hashes(self, num_hashes):
        self.hashes = []
        for i in range(num_hashes):
            self.hashes.append(functools.partial(mmh3.hash, seed=i))
        return self.hashes

    def filter(self, m):
        for hashFun in self.hashes:
            pos = hashFun(m) % len(self.array)
            if self.array[pos] == 0:
                return False
        return True

    def filter_all(self, emails):
        errors = 0
        for email in emails:
            if self.filter(email):
                print("Email Passed")
                errors += 1
        return errors

    def reset(self):
        self.array.setall(0)
        self.num_hashes = 0
        self.hashes = []
