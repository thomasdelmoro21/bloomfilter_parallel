import pandas as pd
import matplotlib.pyplot as plt

from test import test_key, time_par_key, time_seq_key, speedup_key, fpr_key


def plot():
    # Read the setup.csv file
    fprs = ['001', '005', '010']
    for fpr in fprs:
        df = pd.read_csv('./csv/joblib/'+fpr+'/setup.csv', sep=',')

        tests = [2, 4, 6, 8, 10, 12, 14, 16]
        # Plot execution times
        plt.figure()
        plt.title('Setup: Execution times')
        plt.plot(df[test_key], df[time_seq_key], '-o', label='Sequential')
        for i in tests:
            plt.plot(df[test_key], df[time_par_key+str(i)], '-o', label='{} Threads'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Time (s)')
        plt.tight_layout()
        plt.legend()
        plt.grid()
        plt.savefig('./csv/joblib/'+str(fpr)+'/setup_time_plot.png')

        # Plot speedup
        plt.figure()
        plt.title('Setup: Speedup')
        plt.plot(df[test_key], df[time_seq_key]/df[time_seq_key], '-o', label='Sequential')
        for i in tests:
            plt.plot(df[test_key], df[speedup_key+str(i)], '-o', label='{} Threads'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Speedup')
        plt.legend()
        plt.tight_layout()
        plt.grid()
        plt.savefig('./csv/joblib/'+str(fpr)+'/setup_speedup_plot.png')

        # Plot FPR
        plt.figure()
        plt.title('Setup: False Positive Rate')
        plt.plot(df[test_key], df[fpr_key], '-o')
        plt.xlabel('Selected emails')
        plt.ylabel('FPR')
        plt.tight_layout()
        plt.grid()
        plt.savefig('./csv/joblib/'+str(fpr)+'/setup_fpr_plot.png')

        # Read the filter.csv file
        df = pd.read_csv('./csv/joblib/'+str(fpr)+'/filter.csv', sep=',')

        # Plot times Filter
        plt.figure()
        plt.title('Filter: Execution times')
        plt.plot(df[test_key], df[time_seq_key], '-o', label='Sequential')
        for i in tests:
            plt.plot(df[test_key], df[time_par_key+str(i)], '-o', label='{} Threads'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Time (s)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/'+str(fpr)+'/filter_time_plot.png')

        # Plot speedup Filter
        plt.figure()
        plt.title('Filter: Speedup')
        plt.plot(df[test_key], df[time_seq_key]/df[time_seq_key], '-o', label='Sequential')
        for i in tests:
            plt.plot(df[test_key], df[speedup_key+str(i)], '-o', label='{} Threads'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Speedup')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/'+str(fpr)+'/filter_speedup_plot.png')

        # Plot FPR
        plt.figure()
        plt.title('Filter: False Positive Rate')
        plt.plot(df[test_key], df[fpr_key], '-o')
        plt.xlabel('Selected emails')
        plt.ylabel('FPR')
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/'+str(fpr)+'/filter_fpr_plot.png')

        # Read the chunks.csv file
        df = pd.read_csv('./csv/joblib/'+str(fpr)+'/chunks.csv', sep=',')

        test_chunks = [(16 * 2 ** i) for i in range(8)]  # Number of chunks to test

        # Plot times Chunks
        plt.figure()
        plt.title('Filter: Execution times')
        plt.plot(df[test_key], df[time_seq_key], '-o', label='Sequential')
        for i in test_chunks:
            plt.plot(df[test_key], df[time_par_key+str(i)], '-o', label='{} Threads'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Time (s)')
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/' + str(fpr) + '/chunks_time_plot.png')

        # Plot speedup Filter
        plt.figure()
        plt.title('Filter: Speedup')
        plt.plot(df[test_key], df[time_seq_key] / df[time_seq_key], '-o', label='Sequential')
        for i in test_chunks:
            plt.plot(df[test_key], df[speedup_key+ str(i)] , '-o', label='{} Threads'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Speedup')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/' + str(fpr) + '/chunks_speedup_plot.png')

        # Plot FPR
        plt.figure()
        plt.title('Filter: False Positive Rate')
        plt.plot(df[test_key], df[fpr_key], '-o')
        plt.xlabel('Selected emails')
        plt.ylabel('FPR')
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/' + str(fpr) + '/chunks_fpr_plot.png')


def replot_chunks():
    fprs = ['001', '005', '010']
    for fpr in fprs:
        # Read the chunks.csv file
        df = pd.read_csv('./csv/joblib/' + str(fpr) + '/chunks.csv', sep=',')

        test_chunks = [(16 * 2 ** i) for i in range(8)]  # Number of chunks to test

        # Plot times Chunks
        plt.figure()
        plt.title('Filter: Execution times')
        plt.plot(df[test_key], df[time_seq_key], '-o', label='Sequential')
        for i in test_chunks:
            plt.plot(df[test_key], df[time_par_key + str(i)], '-o', label='{} Chunks'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Time (s)')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/' + str(fpr) + '/chunks_time_plot.png')

        # Plot speedup Filter
        plt.figure()
        plt.title('Filter: Speedup')
        plt.plot(df[test_key], df[time_seq_key] / df[time_seq_key], '-o', label='Sequential')
        for i in test_chunks:
            plt.plot(df[test_key], df[speedup_key + str(i)], '-o', label='{} Chunks'.format(i))
        plt.xlabel('Selected emails')
        plt.ylabel('Speedup')
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/' + str(fpr) + '/chunks_speedup_plot.png')

        # Plot FPR
        plt.figure()
        plt.title('Filter: False Positive Rate')
        plt.plot(df[test_key], df[fpr_key], '-o')
        plt.xlabel('Selected emails')
        plt.ylabel('FPR')
        plt.grid()
        plt.tight_layout()
        plt.savefig('./csv/joblib/' + str(fpr) + '/chunks_fpr_plot.png')


if __name__ == '__main__':
    # plot()
    replot_chunks()


