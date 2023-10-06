"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import csv

from matplotlib import pyplot as plt

from bloom_filter import BloomFilter
from email_generator import emails_filename, load_emails, spams_filename
from test import *

results_filename = 'results/results.csv'


def main():
    results = {'test': [], 'time_seq': [], 'fpr': []}
    for i in test_threads:
        results['time_par'+str(i)] = []
        results['speedup'+str(i)] = []
    emails = load_emails(emails_filename)
    spam_emails = load_emails(spams_filename)
    print(f"**Number of cores/threads: {n_threads}**")
    for test in test_sizes:
        print(f"TEST: {test}")
        test_emails = emails[:test]
        bloom_filter = BloomFilter(fpr)

        # Sequential
        print("Sequential: ", end='')
        seq_time = bloom_filter.seq_setup(test_emails)
        print(f"{seq_time} seconds")

        seq_bitarray = bloom_filter.bitarray.copy()

        # Parallel
        par_times = {}
        speedups = {}
        for threads in test_threads:
            print(f"Parallel with {threads} threads: ", end='')
            par_time = bloom_filter.par_setup(test_emails, threads)
            print(f"{par_time} seconds")

            # Speedup
            speedup = seq_time / par_time
            print(f"Speedup with {threads} threads {speedup}")

            # Check if arrays are equal
            par_bitarray = bloom_filter.bitarray.copy()
            if not np.array_equal(seq_bitarray, par_bitarray):
                raise Exception("ARRAYS ARE NOT EQUAL")

            # Save parallel results
            par_times[threads] = par_time
            speedups[threads] = speedup

        # False Positive Rate
        errors = bloom_filter.filter_all(spam_emails)
        v_fpr = errors / len(spam_emails)
        print(f"Errors {errors} and FPR {v_fpr}")
        print()

        # Save results
        save_results(results_filename, results, test, seq_time, par_times, speedups, v_fpr)

    plot_results(results)


def save_results(filename, results, test, seq_time, par_times, speedups, v_fpr):
    # Save results to dict
    results['test'].append(test)
    results['time_seq'].append(seq_time)
    results['fpr'].append(v_fpr)
    for i in test_threads:
        results['time_par'+str(i)].append(par_times[i])
        results['speedup'+str(i)].append(speedups[i])

    with open(filename, 'w', newline='') as csvfile:
        headers = ['test', 'time_seq', 'fpr']
        for i in test_threads:
            headers.append('time_par'+str(i))
            headers.append('speedup'+str(i))

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for i in range(len(results['test'])):
            row = {}
            for header in headers:
                row[header] = results[header][i]
            writer.writerow(row)


def plot_results(results):
    print(results)
    plt.figure(figsize=(24, 8))

    # Plot times
    plt.subplot(1, 3, 1)
    plt.plot(results['test'], results['time_seq'], marker='o', label='Sequential')
    for i in test_threads:
        plt.plot(results['test'], results['time_par'+str(i)], marker='o', label=f'Parallel {i} Threads')
    plt.xlabel('Test Sizes')
    plt.ylabel('Time (seconds)')
    plt.title(f'Time vs. Test Sizes)')
    plt.legend()

    # Plot speedup
    plt.subplot(1, 3, 2)
    for i in test_threads:
        plt.plot(results['test'], results['speedup'+str(i)], marker='o', label=f'Parallel {i} Threads')
    plt.xlabel('Test Sizes')
    plt.ylabel('Speedup')
    plt.title(f'Speedup vs. Test Sizes')
    plt.legend()

    # Plot false positive rate
    plt.subplot(1, 3, 3)
    plt.plot(results['test'], results['fpr'], marker='o', label='False Positive Rate')
    plt.xlabel('Test Sizes')
    plt.ylabel('False Positive Rate (%)')
    plt.title(f'FPR vs. Test Sizes')
    plt.legend()

    plt.tight_layout()
    plt.savefig('plots/result.png')
    plt.show()


if __name__ == '__main__':
    main()
