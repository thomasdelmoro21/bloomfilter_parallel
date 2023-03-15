from bitarray import bitarray
import re


class BloomFilter:

    def __init__(self, size, set):
        self.array = bitarray(size)
        self.array.setall(0)
        self.hashes = self.setHashes()
        self.setup(set)

    def setHashes(self):
        def hash1(m):
            return len(m)

        def hash2(m):
            return len(m) ^ 2

        def hash3(m):
            vowels = re.findall("a|e|i|o|u|y", m)
            return len(vowels) ^ 3

        def hash4(m):
            consonants = re.findall("b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|w|x|z", m)
            return len(consonants) ^ 3

        def hash5(m):
            numbers = re.findall("[0-9]", m)
            return len(numbers) * 600

        return [hash1, hash2, hash3, hash4, hash5]

    def setup(self, set):
        for m in set:
            for hashFun in self.hashes:
                self.array[hashFun(m)] = 1

    def filter(self, m):
        for hashFun in self.hashes:
            if self.array[hashFun(m)] == 0:
                return False
        return True
