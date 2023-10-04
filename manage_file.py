import os

file_name = "dataset/emails/emails_"
spam_file_name = "dataset/spam/spam_"


def import_emails(file_name, test):
    with open(f"{file_name}{test}.txt", 'r') as file:
        emails = file.read().splitlines()
    return emails


def import_spam_emails(file_name, test):
    with open(f"{file_name}{test}_100.txt", 'r') as file:
        emails = file.read().splitlines()
    return emails


def export_emails(emails, test_size):
    with open(os.path.join(f'{file_name}{test_size}.txt'), 'w') as f:
        for email in emails:
            f.write(f"{email}\n")


def export_spam_emails(spam_emails, test_size, spam_size):
    with open(os.path.join(f'{spam_file_name}{test_size}_{spam_size}.txt'), 'w') as f:
        for email in spam_emails:
            f.write(f"{email}\n")
