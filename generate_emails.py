"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

import random


def generate_emails(test_size):
    emails = []
    for i in range(test_size):
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
        emails.append(email)

    with open(f'./email_{test_size}.txt', 'w') as f:
        for email in emails:
            f.write(f"{email}\n")

    mailSet = random.sample(emails, 10000)
    return mailSet
