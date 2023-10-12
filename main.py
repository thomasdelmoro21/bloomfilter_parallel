"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import csv

from matplotlib import pyplot as plt

from bloom_filter import BloomFilter
from email_generator import emails_filename, load_emails, spams_filename
from test import *


def main():
    setup_results = {
        test_key: [],
        time_seq_key: [],
        **{f'{time_par_key}{i}': [] for i in test_threads},
        **{f'{speedup_key}{i}': [] for i in test_threads}
    }

    filter_results = {
        test_key: [],
        time_seq_key: [],
        fpr_key: [],
        **{f'{time_par_key}{i}': [] for i in test_threads},
        **{f'{speedup_key}{i}': [] for i in test_threads}
    }

    # Load emails
    emails = load_emails(emails_filename)
    spam_emails = load_emails(spams_filename)

    bloom_filter = BloomFilter(fpr)

    print(f"***NUMBER OF CORES/THREADS: {n_threads}***\n")
    for test in test_sizes:
        print(f"\n**TEST: {test}")
        test_emails = emails[:test]

        # Sequential
        print("Sequential: ", end='')
        seq_setup_time = bloom_filter.seq_setup(test_emails)
        print(f"{seq_setup_time} seconds")

        seq_bitarray = bloom_filter.bitarray.copy()

        # Parallel
        par_times = {}
        speedups = {}
        for threads in test_threads:
            print(f"Parallel with {threads} threads: ", end='')
            par_setup_time = bloom_filter.par_setup(test_emails, threads)
            print(f"{par_setup_time} seconds")

            # Speedup
            speedup = seq_setup_time / par_setup_time
            print(f"Speedup with {threads} threads {speedup}")

            # Check if arrays are equal
            par_bitarray = bloom_filter.bitarray.copy()
            if not np.array_equal(seq_bitarray, par_bitarray):
                raise Exception("ARRAYS ARE NOT EQUAL")

            # Save parallel results
            par_times[threads] = par_setup_time
            speedups[threads] = speedup

        # Save results
        save_results(setup_results_filename, setup_results, test, seq_setup_time, par_times, speedups)

    plot_results(setup_results)

    for test in spam_sizes:
        print(f"\n**FILTER TEST: {test} spam emails")
        test_emails = spam_emails[:test]

        print(f"Filter Sequential: ", end='')
        seq_filter_time, seq_errors = bloom_filter.filter_all_seq(test_emails)
        print(f"{seq_filter_time} seconds")

        par_filter_times = {}
        filter_speedups = {}
        for threads in test_threads:
            print(f"Filter Parallel with {threads} threads: ", end='')
            par_filter_time, par_errors = bloom_filter.filter_all_par(test_emails, threads)
            print(f"{par_filter_time} seconds")
            speedup = seq_filter_time / par_filter_time
            print(f"Speedup with {threads} threads {speedup}")

            if seq_errors != par_errors:
                raise Exception("DIFFERENT ERROR RATES")

            par_filter_times[threads] = par_filter_time
            filter_speedups[threads] = speedup

        v_fpr = seq_errors / len(test_emails)
        print(f"Errors {seq_errors} and FPR {v_fpr}\n")

        save_results(filter_results_filename, filter_results, test, seq_filter_time, par_filter_times, filter_speedups,
                     v_fpr)

    plot_results(filter_results, filter=True)

def save_results(filename, results, test, seq_time, par_times, speedups, v_fpr=None):
    # Save results
    results[test_key].append(test)
    results[time_seq_key].append(seq_time)
    [results[time_par_key + str(i)].append(par_times[i]) for i in test_threads]
    [results[speedup_key + str(i)].append(speedups[i]) for i in test_threads]
    if v_fpr is not None:
        results[fpr_key].append(v_fpr)

    # Save to csv
    with (open(filename, 'w', newline='') as csvfile):
        if v_fpr is not None:
            headers = [test_key, time_seq_key, fpr_key]
        else:
            headers = [test_key, time_seq_key]
        headers += [key for i in test_threads for key in [time_par_key + str(i), speedup_key + str(i)]]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        [writer.writerow({header: results[header][i] for header in headers}) for i in range(len(results[test_key]))]


def plot_results(results, filter=False):
    print(results)
    plt.figure(figsize=(24, 8))

    if filter:
        # Plot times
        plt.subplot(1, 3, 1)
        plt.plot(results[test_key], results[time_seq_key], marker='o', label='Sequential')
        for i in test_threads:
            plt.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i} Threads')
        plt.xlabel('Test Sizes')
        plt.ylabel('Time (seconds)')
        plt.title('Time vs. Test Sizes)')
        plt.legend()

        # Plot speedup
        plt.subplot(1, 3, 2)
        for i in test_threads:
            plt.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i} Threads')
        plt.xlabel('Test Sizes')
        plt.ylabel('Speedup')
        plt.title('Speedup vs. Test Sizes')
        plt.legend()

        # Plot false positive rate
        plt.subplot(1, 3, 3)
        plt.plot(results[test_key], results[fpr_key], marker='o', label='False Positive Rate')
        plt.xlabel('Test Sizes')
        plt.ylabel('False Positive Rate')
        plt.title('FPR vs. Test Sizes')
        plt.legend()

        plt.tight_layout()
        plt.savefig(plot_filter_filename)

    else:
        plt.subplot(1, 2, 1)
        plt.plot(results[test_key], results[time_seq_key], marker='o', label='Sequential')
        for i in test_threads:
            plt.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i} Threads')
        plt.xlabel('Test Sizes')
        plt.ylabel('Time (seconds)')
        plt.title('Time vs. Test Sizes')
        plt.legend()

        # Plot speedup
        plt.subplot(1, 2, 2)
        for i in test_threads:
            plt.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i} Threads')
        plt.xlabel('Test Sizes')
        plt.ylabel('Speedup')
        plt.title('Speedup vs. Test Sizes')
        plt.legend()

        plt.tight_layout()
        plt.savefig(plot_setup_filename)

    plt.show()


if __name__ == '__main__':
    main()
