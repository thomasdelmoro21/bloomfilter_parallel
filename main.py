"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import os

from bloom_filter import BloomFilter


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
    n_threads = os.cpu_count()
    print(f"**Number of cores/threads: {n_threads}**")
    for n_thread in range(2, n_threads, 2):
        print(f"Number of cores/threads used: {n_thread}")
        for test in test_sizes:
            print(f"TEST {test}")
            emails = import_emails(file_name, test)
            bloom_filter = BloomFilter(filter_size)

            t_seq = bloom_filter.setup(emails)
            print(f"Sequential {t_seq}")

            bloom_filter.reset()

            t_par = bloom_filter.parallel_setup(emails, n_thread)
            print(f"Parallel {t_par}")

            speedup = t_seq/t_par
            print(f"Speedup {speedup}")

            spam_emails = import_spam_emails(spam_file_name, test)
            errors = bloom_filter.filter_all(spam_emails)
            print("\n")


if __name__ == '__main__':
    main()

