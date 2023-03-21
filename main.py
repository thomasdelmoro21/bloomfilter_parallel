"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

import random
from bloom_filter import BloomFilter

def main():

    mailSet = random.sample(emails, 1000)
    filterSize = 10000
    bloomFilter = BloomFilter(filterSize, mailSet)

    goodMail = mailSet[5]
    MaybeSpamEmail = emails[997]

    with open('./email.txt', 'r') as f:
        emails = f.read().splitlines()

    print(emails)


    print(bloomFilter.filter(goodMail))
    print(bloomFilter.filter(MaybeSpamEmail))

    print(bloomFilter.array)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
