import csv

from matplotlib import pyplot as plt

from test import test_key, time_seq_key, time_par_key, speedup_key, plot_chunks_filename, plot_setup_filename, \
     plot_filter_filename, fpr_key


def save_results(filename, results, test, seq_time, tests, par_times, speedups, v_fpr=None):
    # Save results
    results[test_key].append(test)
    results[time_seq_key].append(seq_time)
    [results[time_par_key + str(i)].append(par_times[i]) for i in tests]
    [results[speedup_key + str(i)].append(speedups[i]) for i in tests]
    if v_fpr is not None:
        results[fpr_key].append(v_fpr)

    # Save to csv
    with (open(filename, 'w', newline='') as csvfile):
        if v_fpr is not None:
            headers = [test_key, time_seq_key, fpr_key]
        else:
            headers = [test_key, time_seq_key]
        headers += [key for i in tests for key in [time_par_key + str(i), speedup_key + str(i)]]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        [writer.writerow({header: results[header][i] for header in headers}) for i in range(len(results[test_key]))]


def plot_setup_results(results, tests):
    print(results)
    fig, (times, speedups) = plt.subplots(1, 2, figsize=(16, 8))

    # Plot times
    times.plot(results[test_key], results[time_seq_key], marker='o', label='Sequential')
    for i in tests:
        times.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i} Threads')
    times.set_xlabel('Test Sizes')
    times.set_ylabel('Time (seconds)')
    times.set_title('Time vs. Test Sizes')
    times.legend()

    # Plot speedup
    for i in tests:
        speedups.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i} Threads')
    speedups.set_xlabel('Test Sizes')
    speedups.set_ylabel('Speedup')
    speedups.set_title('Speedup vs. Test Sizes')
    speedups.legend()

    # Save plot
    plt.tight_layout()
    plt.savefig(plot_setup_filename)
    plt.show()


def plot_filter_results(results, tests):
    print(results)
    fig, (times, speedups, fprs) = plt.subplots(1, 3, figsize=(24, 8))

    # Plot times
    times.plot(results[test_key], results[time_seq_key], marker='o', label='Sequential')
    for i in tests:
        times.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i} Threads')
    times.set_xlabel('Test Sizes')
    times.set_ylabel('Time (seconds)')
    times.set_title('Time vs. Test Sizes')
    times.legend()

    # Plot speedup
    for i in tests:
        speedups.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i} Threads')
    speedups.set_xlabel('Test Sizes')
    speedups.set_ylabel('Speedup')
    speedups.set_title('Speedup vs. Test Sizes')
    speedups.legend()

    # Plot false positive rate
    fprs.plot(results[test_key], results[fpr_key], marker='o', label='False Positive Rate')
    fprs.set_xlabel('Test Sizes')
    fprs.set_ylabel('False Positive Rate')
    fprs.set_title('FPR vs. Test Sizes')
    fprs.legend()

    # Save plot
    plt.tight_layout()
    plt.savefig(plot_filter_filename)
    plt.show()


def plot_chunks_results(results, tests):
    print(results)
    fig, (times, speedups) = plt.subplots(1, 2, figsize=(16, 8))

    # Plot times
    for i in tests:
        times.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i} Chunks')
    times.set_xlabel('Test Sizes')
    times.set_ylabel('Time (seconds)')
    times.set_title('Time vs. Test Sizes')
    times.legend()

    # Plot speedup
    for i in tests:
        speedups.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i} Chunks')
    speedups.set_xlabel('Test Sizes')
    speedups.set_ylabel('Speedup')
    speedups.set_title('Speedup vs. Test Sizes')
    speedups.legend()

    # Save plot
    plt.tight_layout()
    plt.savefig(plot_chunks_filename)
    plt.show()
