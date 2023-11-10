import pandas as pd
from matplotlib import pyplot as plt

setup_results = 'results/csv/omp/setup.csv'
filter_results = 'results/csv/omp/filter.csv'

plot_setup_filename = 'results/plots/omp/setup_'
plot_filter_filename = 'results/plots/omp/filter_'


def plot_csv_data(csv_filename, plot_filename):
    data = pd.read_csv(csv_filename, delimiter=';')

    test_key = 'test'
    time_seq_key = 'tSeq'
    time_par_keys = [f'tPar{i}' for i in range(2, len(data.columns) - 2, 2)]
    speedup_keys = [f'speedUp{i}' for i in range(2, len(data.columns) - 2, 2)]
    fpr_key = 'fpr'

    # Plot Times
    plt.figure()
    plt.plot(data[test_key], data[time_seq_key], marker='o', label='Sequential')
    for i, time_par_key in enumerate(time_par_keys):
        plt.plot(data[test_key], data[time_par_key], marker='o', label=f'Parallel {i*2 + 2} Threads')
    plt.xlabel('Dimensioni del Test')
    plt.ylabel('Tempo (secondi)')
    plt.title('Tempo vs. Dimensioni del Test')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(plot_filename + 'time_plot.png')
    # plt.show()

    # Plot Speedup
    plt.figure()
    for i, speedup_key in enumerate(speedup_keys):
        plt.plot(data[test_key], data[speedup_key], marker='o', label=f'Parallel {i*2 + 2} Threads')
    plt.xlabel('Dimensioni del Test')
    plt.ylabel('Speedup')
    plt.title('Speedup vs. Dimensioni del Test')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(plot_filename + 'speedup_plot.png')
    # plt.show()

    # Plot FPR
    plt.figure()
    plt.plot(data[test_key], data[fpr_key], marker='o', label='False Positive Rate')
    plt.xlabel('Dimensioni del Test')
    plt.ylabel('False Positive Rate')
    plt.title('FPR vs. Dimensioni del Test')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(plot_filename + 'fpr_plot.png')
    # plt.show()


def main():
    plot_csv_data(setup_results, plot_filename=plot_setup_filename)
    plot_csv_data(filter_results,  plot_filename=plot_filter_filename)


if __name__ == '__main__':
    main()
