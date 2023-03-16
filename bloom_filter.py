"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

import functools
import math
from bitarray import bitarray
import re
import mmh3


class BloomFilter:

    def __init__(self, size, set):
        self.array = bitarray(size)
        self.array.setall(0)
        self.size = size
        numHashes = int((size / len(set)) * math.log(2))
        print(numHashes)
        self.hashes = self.setHashes(numHashes)
        self.setup(set)

    def setHashes(self, numHashes):
        '''
        def hash1(m):
            return len(m) ^ 2

        def hash2(m):
            return (len(m) * 15) ^ 3

        def hash3(m):
            vowels = re.findall("a|e|i|o|u|y", m)
            return (len(vowels)*20) ^ 5 % self.size

        def hash4(m):
            consonants = re.findall("b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z", m)
            return (len(consonants)*20) ^ 5 % self.size

        def hash5(m):
            numbers = re.findall("[0-9]", m)
            return (len(numbers) * 1000) % self.size

        def hash6(m):
            numbers = re.findall("[0-9]", m)
            consonants = re.findall("b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z", m)
            return (len(numbers)*2 + len(consonants)*10) % self.size

        def hash7(m):
            return (m.count("a") + 6) * 2500 % self.size

        return [hash1, hash2, hash3, hash4, hash5, hash6, hash7]
        '''
        hashes = []
        for i in range(numHashes):
            hashes.append(functools.partial(mmh3.hash, seed=i))
        return hashes
    def setup(self, set):
        for m in set:
            for hashFun in self.hashes:
                pos = hashFun(m) % len(self.array)
                self.array[pos] = 1

    def filter(self, m):
        for hashFun in self.hashes:
            pos = hashFun(m) % len(self.array)
            if self.array[pos] == 0:
                return False
        return True
