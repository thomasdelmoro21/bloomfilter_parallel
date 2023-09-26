"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

import functools
import math
from bitarray import bitarray
import mmh3


class BloomFilter:

    def __init__(self, size):
        self.size = size
        self.array = bitarray(size)
        self.array.setall(0)
        self.num_hashes = 0
        self.hashes = []

    def setup(self, emails):
        self.num_hashes = int((self.size / len(emails)) * math.log(2))
        self.hashes = self.set_hashes(self.num_hashes)
        for m in emails:
            for hashFun in self.hashes:
                pos = hashFun(m) % len(self.array)
                self.array[pos] = 1

    def set_hashes(self, num_hashes):
        self.hashes = []
        for i in range(num_hashes):
            self.hashes.append(functools.partial(mmh3.hash, seed=i))
        return self.hashes

    def filter_all(self, emails):
        errors = 0
        for email in emails:
            if self.filter(email):
                print("Email Passed")
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
