"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

from bloom_filter import BloomFilter
from joblib import Parallel, delayed


def import_emails(file_name, test):
    with open(f"{file_name}{test}.txt", 'r') as file:
        emails = file.read().splitlines()
    return emails


def import_spam_emails(file_name, test):
    with open(f"{file_name}{test}_100.txt", 'r') as file:
        emails = file.read().splitlines()
    return emails


def main():
    file_name = "dataset/emails/emails_"
    spam_file_name = "dataset/spam/spam_"
    test_sizes = [1000, 10000, 100000, 1000000]
    spam_size = 100
    filter_size = 8000000
    for test in test_sizes:
        print(f"TEST {test}")
        emails = import_emails(file_name, test)
        print("Setup BloomFilter")
        bloom_filter = BloomFilter(filter_size)

        print("Sequential")
        bloom_filter.setup(emails)

        print("Reset")
        bloom_filter.reset()

        print("Parallel")
        Parallel()(delayed(bloom_filter.setup(emails)))
        spam_emails = import_spam_emails(spam_file_name, test)
        errors = bloom_filter.filter_all(spam_emails)
        # print(errors)


if __name__ == '__main__':
    main()

