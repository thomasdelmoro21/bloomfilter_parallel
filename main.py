"""
@authors
Thomas Del Moro & Lorenzo Baiardi
"""

from bloom_filter import BloomFilter
from generate_emails import generate_emails


def main():
    test_sizes = [10000, 100000]
    for test_size in test_sizes:
        mail_set = generate_emails(test_size)
        bloom_filter = BloomFilter(mail_set)

        with open(f'./email_{test_size}.txt', 'r') as f:
            emails = f.read().splitlines()

        filtered_emails = bloom_filter.filter_emails(emails)

        print(filtered_emails)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
