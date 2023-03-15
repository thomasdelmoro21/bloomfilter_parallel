# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
from bloom_filter import BloomFilter

def main():
    emails = []
    for i in range(100000):
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

    mailSet = random.sample(emails, 1000)
    filterSize = 10000
    bloomFilter = BloomFilter(filterSize, mailSet)

    goodMail = mailSet[500]
    MaybeSpamEmail = emails[997]

    print(bloomFilter.filter(goodMail))
    print(bloomFilter.filter(MaybeSpamEmail))


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
