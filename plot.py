import csv

from matplotlib import pyplot as plt

from test import test_key, time_seq_key, time_par_key, speedup_key, fpr_key


def save_results(filename, results, test, seq_time, tests, par_times, speedups, v_fpr):
    # Save results
    results[test_key].append(test)
    results[time_seq_key].append(round(seq_time,3))
    [results[time_par_key + str(i)].append(round(par_times[i], 3)) for i in tests]  # Limit to 3 decimal digits
    [results[speedup_key + str(i)].append(round(speedups[i], 3)) for i in tests]  # Limit to 3 decimal digits
    results[fpr_key].append(round(v_fpr, 3))  # Limit to 3 decimal digits

    # Save to csv
    with (open(filename, 'w', newline='') as csvfile):
        headers = [test_key, time_seq_key, fpr_key]
        headers += [key for i in tests for key in [time_par_key + str(i), speedup_key + str(i)]]
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        [writer.writerow({header: results[header][i] for header in headers}) for i in range(len(results[test_key]))]


def plot_results(results, filename, tests):
    # print(results)

    # Plot times
    plt.figure()
    plt.plot(results[test_key], results[time_seq_key], marker='o', label='Sequential')
    for i in tests:
        plt.plot(results[test_key], results[time_par_key + str(i)], marker='o', label=f'Parallel {i}')
    plt.xlabel('Test Sizes')
    plt.ylabel('Time (seconds)')
    plt.title('Time vs. Test Sizes')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(filename + 'time_plot.png')
    # plt.show()

    # Plot speedup
    plt.figure()
    for i in tests:
        plt.plot(results[test_key], results[speedup_key + str(i)], marker='o', label=f'Parallel {i}')
    plt.xlabel('Test Sizes')
    plt.ylabel('Speedup')
    plt.title('Speedup vs. Test Sizes')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(filename + 'speedup_plot.png')
    # plt.show()

    # Plot false positive rate
    plt.figure()
    plt.plot(results[test_key], results[fpr_key], marker='o', label='False Positive Rate')
    plt.xlabel('Test Sizes')
    plt.ylabel('False Positive Rate')
    plt.title('FPR vs. Test Sizes')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(filename + 'fpr_plot.png')
    # plt.show()


