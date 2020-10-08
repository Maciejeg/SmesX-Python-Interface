import argparse
import re
import os
import sys
import requests
import csv


class SMS:
    def __init__(self, phone_number, text, user, password, sender=""):
        self.phone_number = phone_number
        self.text = text
        self.sender = sender
        self.user = user
        self.password = password

    phone_number = ""
    text = ""
    sender = ""
    user = ""
    password = ""

    raw_message = ""
    url = 'https://smesx1.smeskom.pl:2200/smesx'

    valid = False

    def validate(self):
        check = True
        if not re.findall(r'\+48\d{9}|^\d{9}', self.phone_number):
            check = False
        elif self.sender != "":
            if not re.findall(r'^[A-z0-9]{1,11}$', self.sender):
                check = False
        return check

    def compose(self):
        self.raw_message = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <request version="2.0" user="{}" password="{}">
                <send_sms>
                    <sender>{}</sender>
                    <msisdn>{}</msisdn>
                    <body>{}</body>
                </send_sms>
            </request>
            '''.format(self.user,
                       self.password,
                       self.sender,
                       self.phone_number,
                       self.text)

    def send(self):
        self.valid = self.validate()
        if self.valid:
            self.compose()
            status = requests.post(self.url, {'xml': self.raw_message})
            status = re.search(r'<execution_status>(.*?)</execution_status>',
                               status.text).group(1)
            return status
        return self.valid


parser = argparse.ArgumentParser(description='SmesX Python Interface help')

parser.add_argument('username',
                    type=str,
                    help='A required username string argument')
parser.add_argument('password',
                    type=str,
                    help='A required password string argument')
parser.add_argument('phone_number',
                    type=str,
                    help='Phone number.'
                         'Example: "+48 123 123 123" or "+48123123123"')
parser.add_argument('-T',
                    '--text',
                    type=str,
                    help="Text message")
parser.add_argument('-C',
                    '--csv',
                    type=str,
                    help="CSV file with sms data. "
                         "CSV structure: phone_number,text,sender_name")
parser.add_argument('-S',
                    '--sender',
                    type=str,
                    help="An optional sender name."
                         "If not specified, default will be used.")

args = parser.parse_args()

EXIT = False

if not args.text:
    if args.csv:
        if not os.path.exists(args.csv):
            print("Wrong CSV directory")
            EXIT = True

if args.sender:
    if re.findall(r'^[A-z0-9]{1,11}$', args.sender):
        pass
    else:
        print("Wrong sender name. "
              "Alphanumeric Sender IDs may be "
              "a maximum of 11 characters in length.")
        EXIT = True

if not args.username or not args.password:
    print("Wrong username or password")
    EXIT = True

if not re.findall(r'\+48\d{9}|^\d{9}', args.phone_number):
    print("Wrong phone number")
    EXIT = True

if EXIT:
    print("SMS not sent")
    sys.exit()

messages = []

if args.csv:
    with open(args.csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            message = SMS(row[0],
                          row[1],
                          args.username,
                          args.password,
                          sender=row[2] or args.sender or "")
            messages.append(message)

for message in messages:
    print(message.send())
