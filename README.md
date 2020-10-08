# SmesX-Python-Interface

SmesX-Python-Interface is a Python script for sending sms via Smeskom's SMS Gateway.

## Installation

TODO

## Usage
```bash
python send_sms.py username password -P 123456789 -T sample_text -C tests\sms.csv
```
### SmesX Python Interface help
```bash
positional arguments:
  username              A required username string argument
  password              A required password string argument

optional arguments:
  -h, --help            show this help message and exit
  -P PHONE_NUMBER, --phone_number PHONE_NUMBER
                        Phone number.Example: "+48 123 123 123" or "+48123123123"
  -T TEXT, --text TEXT  Text message
  -C CSV, --csv CSV     CSV file with sms data. CSV structure: phone_number,text,sender_name
  -S SENDER, --sender SENDER
                        An optional sender name.If not specified, default will be used.
```

## Contributing
Feel free to contribute

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)