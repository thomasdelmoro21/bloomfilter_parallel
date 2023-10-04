import time

from joblib import Parallel, delayed
import numpy as np
import os
import tempfile
import shutil


def main():
    print("Nested loop array assignment:")
    start = time.time()
    regular()
    print("Time: " + str(time.time() - start))
    print("Parallel nested loop assignment using numpy's memmap:")
    start = time.time()
    par3(4)
    print("Time: " + str(time.time() - start))


def regular():
    # Define variables
    a = np.arange(0, 10000)
    b = np.arange(0, 1000)

    # Set array variable to global and define size and shape
    global ab
    ab = np.zeros((2, np.size(a), np.size(b)))

    # Iterate to populate array
    for i in range(0, np.size(a)):
        for j in range(0, np.size(b)):
            func(i, j, a, b)

    # Show array output
    print(ab)


def par3(process):
    # Creat a temporary directory and define the array path
    path = tempfile.mkdtemp()
    ab3path = os.path.join(path, 'ab3.mmap')

    # Define variables
    a3 = np.arange(0, 10000)
    b3 = np.arange(0, 1000)

    # Create the array using numpy's memmap
    ab3 = np.memmap(ab3path, dtype=float, shape=(2, np.size(a3), np.size(b3)), mode='w+')

    # Parallel process in order to populate array
    Parallel(n_jobs=process)(delayed(func3)(i, a3, b3, ab3) for i in range(0, np.size(a3)))

    # Show array output
    print(ab3)

    # Delete the temporary directory and contents
    try:
        shutil.rmtree(path)
    except:
        print("Couldn't delete folder: " + str(path))


def func(i, j, a, b):
    # Populate array
    ab[0, i, j] = a[i] + b[j]
    ab[1, i, j] = a[i] * b[j]


def func3(i, a3, b3, ab3):
    # Populate array
    for j in range(0, np.size(b3)):
        ab3[0, i, j] = a3[i] + b3[j]
        ab3[1, i, j] = a3[i] * b3[j]


# Run script
main()
