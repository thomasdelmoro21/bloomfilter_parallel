"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import os

from bloom_filter import BloomFilter
from in_out_file import import_emails, import_spam_emails, file_name, spam_file_name
from test import *


def main():
    n_threads = os.cpu_count()
    print(f"**Number of cores/threads: {n_threads}**")
    for n_thread in range(2, n_threads+1, 2):
        print(f"Number of cores/threads used: {n_thread}")
        for test in test_sizes:
            print(f"TEST {test}")
            emails = import_emails(file_name, test)
            bloom_filter = BloomFilter(filter_size)

            t_seq = bloom_filter.setup(emails)
            seq_array = bloom_filter.array
            print(f"Sequential {t_seq}")

            bloom_filter.reset()

            t_par = bloom_filter.parallel_setup(emails, n_thread)
            par_array = bloom_filter.array
            print(f"Parallel {t_par}")

            speedup = t_seq/t_par
            print(f"Speedup {speedup}")

            # compare arrays
            if seq_array == par_array:
                print("Bit arrays are equal (sequential and parallel)")

            spam_emails = import_spam_emails(spam_file_name, test)
            errors = bloom_filter.filter_all(spam_emails)
            print(f"Errors {errors} and FPR {errors/len(spam_emails)*100}")
            print()


if __name__ == '__main__':
    main()
