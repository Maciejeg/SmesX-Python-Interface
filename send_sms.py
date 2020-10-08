import argparse
import csv
import os
import re
import requests
import sys


class SMS:
    """SMS class"""
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
    """SMS gateway url"""
    url = 'https://smesx1.smeskom.pl:2200/smesx'

    valid = False

    """Validate SMS data"""
    def validate(self):
        check = True
        """Basic phone number regex validation"""
        if not re.findall(r'\+48\d{9}|^\d{9}', self.phone_number):
            check = False
        elif self.sender != "":
            self.sender = self.sender.replace(' ', '')
            """Sender ID valdation"""
            if not re.findall(r'^[A-z0-9]{1,11}$', self.sender):
                check = False
        return check

    """Compose request"""
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

    """Validate, Compose and Send SMS"""
    def send(self):
        self.valid = self.validate()
        if self.valid:
            self.compose()
            status = requests.post(self.url, {'xml': self.raw_message})
            try:
                """Search for error code"""
                error_code = re.search(r'<fail_code>(.*?)</fail_code>',
                                       status.text).group(1)
            except AttributeError:
                """Happens if there is no error"""
                error_code = "-"
            try:
                """Search for error description"""
                error_description = re.search(r'<fail_description>(.*?)'
                                              r'</fail_description>',
                                              status.text).group(1)
            except AttributeError:
                """Happens if there is no error"""
                error_description = "-"
            """Search for execution status"""
            status = re.search(r'<execution_status>(.*?)</execution_status>',
                               status.text).group(1)
            result = "Status: {}, Error code: {}, Error description: {}"
            result = result.format(status, error_code, error_description)
            return result
        return self.valid


parser = argparse.ArgumentParser(description='SmesX Python Interface help')

parser.add_argument('username',
                    type=str,
                    help='A required username string argument')
parser.add_argument('password',
                    type=str,
                    help='A required password string argument')
parser.add_argument('-P',
                    '--phone_number',
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

if args.phone_number:
    if not re.findall(r'\+48\d{9}|^\d{9}', args.phone_number):
        print("Wrong phone number")
        EXIT = True

if EXIT:
    print("SMS not sent")
    sys.exit()

messages = []

if args.text and args.phone_number:
    messages.append(SMS(args.phone_number,
                        args.text,
                        args.user,
                        args.password,
                        args.sender or ""))

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
