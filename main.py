"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

from src.bloom_filter import BloomFilter
from src.email_generator import emails_filename, load_emails, spams_filename
from plot import save_results, plot_setup_results, plot_filter_results, plot_chunks_results
from test import *


def setup_test(bloom_filter, emails):
    setup_results = {
        test_key: [],
        time_seq_key: [],
        **{f'{time_par_key}{i}': [] for i in test_threads},
        **{f'{speedup_key}{i}': [] for i in test_threads}
    }

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
        save_results(setup_results_filename, setup_results, test, seq_setup_time, test_threads, par_times, speedups)

    plot_setup_results(setup_results, test_threads)


def filter_test(bloom_filter, spam_emails):
    filter_results = {
        test_key: [],
        time_seq_key: [],
        fpr_key: [],
        **{f'{time_par_key}{i}': [] for i in test_threads},
        **{f'{speedup_key}{i}': [] for i in test_threads}
    }

    for test in spam_sizes:
        print(f"\n**FILTER TEST: {test} spam emails")
        test_emails = spam_emails[:test]

        # Sequential
        print(f"Filter Sequential: ", end='')
        seq_filter_time, seq_errors = bloom_filter.seq_filter_all(test_emails)
        print(f"{seq_filter_time} seconds")

        # Parallel
        par_filter_times = {}
        filter_speedups = {}
        for threads in test_threads:
            print(f"Filter Parallel with {threads} threads: ", end='')
            par_filter_time, par_errors = bloom_filter.par_filter_all(test_emails, threads)
            print(f"{par_filter_time} seconds")

            # Speedup
            speedup = seq_filter_time / par_filter_time
            print(f"Speedup with {threads} threads {speedup}")

            # Check if errors are equal
            if seq_errors != par_errors:
                raise Exception("DIFFERENT ERROR RATES")

            # Save parallel results
            par_filter_times[threads] = par_filter_time
            filter_speedups[threads] = speedup

        v_fpr = seq_errors / len(test_emails)
        print(f"Errors {seq_errors} and FPR {v_fpr}\n")

        save_results(filter_results_filename, filter_results, test, seq_filter_time, test_threads, par_filter_times,
                     filter_speedups, v_fpr)

    plot_filter_results(filter_results, test_threads)


def chunks_setup_test(bloom_filter, emails):
    setup_results = {
        test_key: [],
        time_seq_key: [],
        **{f'{time_par_key}{i}': [] for i in test_chunks},
        **{f'{speedup_key}{i}': [] for i in test_chunks}
    }

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
        save_results(chunks_results_filename, setup_results, test, seq_setup_time, test_chunks, par_times, speedups)

    plot_chunks_results(setup_results, test_chunks)


def main():
    emails = load_emails(emails_filename)
    spams = load_emails(spams_filename)
    bloom_filter = BloomFilter(fpr)

    # Setup
    setup_test(bloom_filter, emails)

    # Filter
    filter_test(bloom_filter, spams)

    # Chunks
    chunks_setup_test(bloom_filter, emails)


if __name__ == '__main__':
    main()
