"""
@authors:
Thomas Del Moro & Lorenzo Baiardi
"""

import os
import pickle
import random
import string
import time

import numpy as np
from joblib import Parallel, delayed

from test import test_sizes, spam_sizes

emails_filename = os.path.join('dataset/emails.pkl')
spams_filename = os.path.join('dataset/spams.pkl')

punctuation = '.-_'
tlds = ['.com', '.net', '.org', '.info', '.it', '.eu', '.biz', '.gov', '.edu', '.co.uk', '.de', '.fr', '.es']
domains = ['@gmail', '@yahoo', '@hotmail', '@libero', '@icloud', '@outlook', '@protonmail', '@alice', '@tiscali',
           '@fastweb', '@virgilio', '@tim', '@vodafone', '@wind', '@telecom', '@poste']

n_emails = max(test_sizes)  # Number of emails
n_spam = max(spam_sizes)  # Number of spam emails


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


def check_duplicates(emails, spam_emails):
    print("Checking for duplicates in the generated emails...")
    print(f"Found {len(emails) - len(set(emails))} duplicates")

    print("Checking for duplicates...")
    check = np.in1d(spam_emails, emails)
    print(f"Found {check.sum()} spam emails in the generated emails")

    print("Removing duplicates...")
    spam_emails = list(set(spam_emails) - set(emails))
    print(f"Removed {check.sum()} duplicates")
    return emails, spam_emails


def main():
    print(f"SEQUENTIAL: Generating {n_emails} emails ", end='')
    start = time.time()
    [generate_email() for _ in range(n_emails)]
    t_seq = time.time() - start
    print(f"in {t_seq} seconds")

    print(f"PARALLEL: Generating {n_emails} emails ", end='')
    start = time.time()
    emails = Parallel(n_jobs=-1)(delayed(generate_email)() for _ in range(n_emails))
    t_par = time.time() - start
    print(f"in {t_par} seconds")

    print(f"Speedup: {t_seq / t_par}")

    print(f"PARALLEL: Generating {n_spam} spam emails ", end='')
    start = time.time()
    spam_emails = Parallel(n_jobs=-1)(delayed(generate_email)(True) for _ in range(n_spam))
    spam_time = time.time() - start
    print(f"in {spam_time} seconds")

    # check_duplicates(emails, spam_emails)

    print("Exporting emails and spam emails...", end='')
    export_emails(emails, emails_filename)
    export_emails(spam_emails, spams_filename)
    print("Done!")
    print(f"Exported {len(emails)} emails to {emails_filename}")
    print(f"Exported {len(spam_emails)} spam emails to {spams_filename}")


if __name__ == '__main__':
    main()
