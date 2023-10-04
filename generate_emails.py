"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

import random
import numpy as np

from in_out_file import export_emails, export_spam_emails


def main():
    test_sizes = [1000, 10000, 100000, 1000000]
    spam_size = 100
    for test_size in test_sizes:
        print(test_size)
        emails = []
        spam_emails = []
        for i in range(test_size):
            emails.append(generation_email())

        for i in range(spam_size):
            spam_emails.append(generation_email())

        print(np.in1d(spam_emails, emails))

        export_emails(emails, test_size)
        export_spam_emails(spam_emails, test_size, spam_size)


def generation_email():
    validchars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    loginlen = random.randint(4, 15)
    login = ''
    for i in range(loginlen):
        pos = random.randint(0, len(validchars) - 1)
        login = login + validchars[pos]
    if login[0].isnumeric():
        pos = random.randint(0, len(validchars) - 10)
        login = validchars[pos] + login
    servers = ['@gmail', '@yahoo', '@hotmail', '@libero', '@icloud']
    servpos = random.randint(0, len(servers) - 1)
    email = login + servers[servpos]
    tlds = ['.com', '.it', '.net', '.org']
    tldpos = random.randint(0, len(tlds) - 1)
    email = email + tlds[tldpos]
    return email


if __name__ == '__main__':
    main()
