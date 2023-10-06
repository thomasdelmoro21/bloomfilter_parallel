"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""
import os
import pickle
import random
import string
import time

import numpy as np
from joblib import Parallel, delayed

from test import test_sizes

emails_filename = os.path.join('dataset/emails.pkl')
spams_filename = os.path.join('dataset/spams.pkl')

punctuation = '.-_'
tlds = ['.com', '.net', '.org', '.info', '.it', '.eu', '.biz', '.gov', '.edu', '.co.uk', '.de', '.fr', '.es']
domains = ['@gmail', '@yahoo', '@hotmail', '@libero', '@icloud', '@outlook', '@protonmail', '@alice', '@tiscali',
           '@fastweb', '@virgilio', '@tim', '@vodafone', '@wind', '@telecom', '@poste']

# Number of spam emails
n_spam = 100000


def load_emails(filename):
    with open(filename, 'rb') as file:
        emails = pickle.load(file)
    return emails


def export_emails(emails, filename):
    with open(filename, 'wb') as file:
        pickle.dump(emails, file)


def generate_email(spam=False):
    if spam:
        lp = 'SPAM'.join(random.choice(string.ascii_letters + string.digits + punctuation)
                         for _ in range(random.randint(5, 40)))
        return f'{lp}@{random.choice(domains)}.{random.choice(tlds)}'
    else:
        while True:
            lp_length = random.randint(5, 40)
            lp = ''.join(random.choice(string.ascii_letters + string.digits + punctuation)
                         for _ in range(lp_length))
            if not lp[0].isdigit() and not lp[0] in punctuation and not lp[-1] in punctuation:
                break
        return f'{lp}@{random.choice(domains)}.{random.choice(tlds)}'


def main():
    n_emails = max(test_sizes)

    print("SEQUENTIAL: Generating {} emails ".format(n_emails), end='')
    start = time.time()
    [generate_email() for _ in range(n_emails)]
    t_seq = time.time() - start
    print("in {} seconds".format(t_seq))

    print("PARALLEL: Generating {} parallel emails ".format(n_emails), end='')
    start = time.time()
    emails = Parallel(n_jobs=-1)(delayed(generate_email)() for _ in range(n_emails))
    t_par = time.time() - start
    print("in {} seconds".format(t_par))

    print("Speedup: {}".format(t_seq / t_par))

    print("PARALLEL: Generating {} spam emails ".format(n_spam), end='')
    start = time.time()
    spam_emails = Parallel(n_jobs=-1)(delayed(generate_email)(True) for _ in range(n_spam))
    spam_time = time.time() - start
    print("in {} seconds".format(spam_time))

    print("Checking for duplicates in the generated emails...")
    print("Found {} duplicates".format(len(emails) - len(set(emails))))

    print("Checking for duplicates...")
    check = np.in1d(spam_emails, emails)
    print("Found {} spam emails in the generated emails".format(check.sum()))

    print("Removing duplicates...")
    spam_emails = list(set(spam_emails) - set(emails))
    print("Removed {} duplicates".format(check.sum()))

    print("Exporting emails and spam emails...")
    export_emails(emails, emails_filename)
    export_emails(spam_emails, spams_filename)
    print("Done!")
    print("Exported {} emails to {}".format(len(emails), emails_filename))
    print("Exported {} spam emails to {}".format(len(spam_emails), spams_filename))


if __name__ == '__main__':
    main()
