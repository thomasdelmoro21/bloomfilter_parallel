"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import csv

from matplotlib import pyplot as plt

from bloom_filter import BloomFilter
from email_generator import emails_filename, load_emails, spams_filename
from test import *

n_threads = os.cpu_count()
test_chunks = [n_threads, n_threads*2, n_threads*4, n_threads*8, n_threads*16, n_threads*32, n_threads*64]


def main():
    setup_results = {
        test_key: [],
        time_seq_key: [],
        **{f'{time_par_key}{i}': [] for i in test_chunks},
        **{f'{speedup_key}{i}': [] for i in test_chunks}
    }

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
        for chunks in test_chunks:
            print(f"Parallel with {chunks} chunks: ", end='')
            par_setup_time = bloom_filter.par_setup(test_emails, n_threads)
            print(f"{par_setup_time} seconds")

            # Speedup
            speedup = seq_setup_time / par_setup_time
            print(f"Speedup with {chunks} chunks {speedup}")

            # Check if arrays are equal
            par_bitarray = bloom_filter.bitarray.copy()
            if not np.array_equal(seq_bitarray, par_bitarray):
                raise Exception("ARRAYS ARE NOT EQUAL")

            # Save parallel results
            par_times[chunks] = par_setup_time
            speedups[chunks] = speedup

        # Save results
        save_results(chunks_results_filename, setup_results, test, seq_setup_time, par_times, speedups)

    plot_results(setup_results)


def save_results(filename, results, test, seq_time, par_times, speedups):
    # Save results
    results[test_key].append(test)
    results[time_seq_key].append(seq_time)
    [results[time_par_key + str(i)].append(par_times[i]) for i in test_chunks]
    [results[speedup_key + str(i)].append(speedups[i]) for i in test_chunks]

    # Save to csv
    with (open(filename, 'w', newline='') as csvfile):
        headers = [test_key, time_seq_key]
        headers += [key for i in test_chunks for key in [time_par_key + str(i), speedup_key + str(i)]]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        [writer.writerow({header: results[header][i] for header in headers}) for i in range(len(results[test_key]))]


def plot_results(results, filter=False):
    print(results)
    plt.figure(figsize=(24, 8))

    plt.subplot(1, 2, 1)
    for i in test_chunks:
        plt.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i} Chunks')
    plt.xlabel('Test Sizes')
    plt.ylabel('Time (seconds)')
    plt.title('Time vs. Test Sizes')
    plt.legend()

    # Plot speedup
    plt.subplot(1, 2, 2)
    for i in test_chunks:
        plt.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i} Chunks')
    plt.xlabel('Test Sizes')
    plt.ylabel('Speedup')
    plt.title('Speedup vs. Test Sizes')
    plt.legend()

    plt.tight_layout()
    plt.savefig(plot_chunks_filename)
    plt.show()


if __name__ == '__main__':
    main()
