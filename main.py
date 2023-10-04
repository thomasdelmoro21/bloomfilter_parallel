"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import numpy as np
from matplotlib import pyplot as plt

from bloom_filter import BloomFilter, BloomFilterOptimized
from generate_emails import generation_email
from test import *


def main():
    results = {}
    print(f"**Number of cores/threads: {n_threads}**")
    for n_thread in test_threads:
        print(f"Number of cores/threads used: {n_thread}")
        for test in test_sizes:
            print(f"TEST {test}")
            emails = [generation_email() for _ in range(test)]
            bloom_filter = BloomFilterOptimized(fpr)

            # Sequential
            t_seq = bloom_filter.seq_setup(emails)
            seq_array = bloom_filter.bit_array.copy()
            print(f"Sequential {t_seq}")

            bloom_filter.reset()

            # Parallel
            t_par = bloom_filter.par_setup(emails, n_thread)
            par_array = bloom_filter.bit_array.copy()
            print(f"Parallel {t_par}")

            # Speedup
            speedup = t_seq / t_par
            print(f"Speedup {speedup}")

            # Check if arrays are equal
            if not np.array_equal(seq_array, par_array):
                raise Exception("Arrays are not equal")
            else:
                print("Arrays are equal")

            # False Positive Rate
            spam_emails = [generation_email() for _ in range(100)]
            errors = bloom_filter.filter_all(spam_emails)
            print(f"Errors {errors} and FPR {errors / len(spam_emails) * 100}")
            print()

            # Save results
            save_results(results, n_thread, test, t_seq, t_par, speedup, errors, spam_emails)

    plot_results(results)


def save_results(results, n_thread, test, t_seq, t_par, speedup, errors, spam_emails):
    if n_thread not in results:
        results[n_thread] = {'test_sizes': [], 'time_seq': [], 'time_par': [], 'speedup': [], 'false_positive_rate': []}

    results[n_thread]['test_sizes'].append(f"TEST{test}")
    results[n_thread]['time_seq'].append(t_seq)
    results[n_thread]['time_par'].append(t_par)
    results[n_thread]['speedup'].append(speedup)
    results[n_thread]['false_positive_rate'].append(errors / len(spam_emails) * 100)


def plot_results(results):
    for n_thread, data in results.items():
        plt.figure(figsize=(12, 6))

        # Plot times
        plt.subplot(2, 2, 1)
        plt.plot(data['test_sizes'], data['time_seq'], marker='o', label='Sequential Time')
        plt.plot(data['test_sizes'], data['time_par'], marker='o', label='Parallel Time')
        plt.xlabel('Test Sizes')
        plt.ylabel('Time (seconds)')
        plt.title(f'Time vs. Test Sizes (Threads: {n_thread})')
        plt.legend()

        # Plot speedup
        plt.subplot(2, 2, 2)
        plt.plot(data['test_sizes'], data['speedup'], marker='o')
        plt.xlabel('Test Sizes')
        plt.ylabel('Speedup')
        plt.title(f'Speedup vs. Test Sizes (Threads: {n_thread})')

        # Plot false positive rate
        plt.subplot(2, 2, 3)
        plt.plot(data['test_sizes'], data['false_positive_rate'], marker='o')
        plt.xlabel('Test Sizes')
        plt.ylabel('False Positive Rate (%)')
        plt.title(f'FPR vs. Test Sizes (Threads: {n_thread})')

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    main()
