#!/usr/bin/env python
# coding=utf-8

"""
Python script whose purpose is to initialize the Mifare Classic 1K Smart Card with some data.

MIT License
Smart Card Contactless Raspberry Pi sample project

Copyright (c) 2022 Antonio Musarra (Antonio Musarra's Blog - https://www.dontesta.it)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "Antonio Musarra"
__copyright__ = "Copyright (c) 2022 Antonio Musarra (Antonio Musarra's Blog - https://www.dontesta.it)"
__credits__ = ["Antonio Musarra"]
__version__ = "1.0.0"
__license__ = "MIT"
__maintainer__ = "Antonio Musarra"
__email__ = "antonio.musarra@gmail.com"
__status__ = "Development"

import argparse
import art
import rpi.smartcard.mifare.mifare_interface as mifare

from rpi import version
from smartcard.util import toHexString
from smartcard.util import toASCIIString
from smartcard.util import toASCIIBytes
from smartcard.util import toBytes
from smartcard.util import padd

# Setup parser argument
parser = argparse.ArgumentParser(description='Smart Card initialization tool.\n This tool is valid for MIFARE Classic '
                                             '1K cards. It must be used to initialize the card with the '
                                             'identification number of the identification document (example: identity '
                                             'card, driving license, social security number, passport number) of the '
                                             'person to whom the card is delivered.')
parser.add_argument("-a", "--authentication-key", help='Authentication Key of Mifare Classic 1K.The authentication '
                                                       'keys are used to authenticate the particular sector of the '
                                                       'MIFARE Classic 1K memory card. Volatile authentication key '
                                                       'location is provided.', required=True)
parser.add_argument("-i", "--document-id", help='Identity document number (example: identity card, driving license, '
                                                'social security number, passport number)', required=True)
args = parser.parse_args()

# Get authentication key for Mifare Classic 1K Smart Card from program arguments
authentication_key = args.authentication_key

# Get Identity document number from program arguments
identification_number = args.document_id


def print_version_info():
    """
    Print the version info about this python script.

    :return: void
    """
    art.tprint("Smart Card Init Tool")
    print("Version: %s" % version.__version__)
    print("Copyright (c) 2022 Antonio Musarra <antonio.musarra@gmail.com>")
    print("Antonio Musarra's Blog - https://www.dontesta.it")
    print("GitHub Project https://github.com/amusarra")
    print("---\n")


def main():
    """
    The main entry point of this python script

    :return: void
    """
    print_version_info()

    mifare_interface = mifare.MifareClassicInterface()
    uid = mifare_interface.get_uid()
    reader = mifare_interface.get_reader()

    print(f"Smart Card Reader: {reader}")
    print(f"Card UID {toHexString(uid)}\n")

    if mifare_interface.load_auth_key(toBytes(authentication_key)):
        if mifare_interface.authentication():
            print("Authentication successful\n")
            print(f"Get previous Identification Number {toASCIIString(mifare_interface.get_document_id())}")
            print(f"Try to store the new Identification Number {identification_number} into Smart Card...")

            result = mifare_interface.set_document_id(
                padd(toASCIIBytes(identification_number), 16, '00')
            )

            if result:
                print(f"The new Identification Number {toASCIIString(mifare_interface.get_document_id())} stored!")
            else:
                print(f"Error on store the Identification Number")
        else:
            print("Authentication failed")
    else:
        print("Load authentication key failed")

    mifare_interface.disconnect()


if __name__ == "__main__":
    main()
