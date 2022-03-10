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
import sys

import art
import rpi.smartcard.mifare.mifare_interface as mifare
import rpi.smartcard.mongodb.smart_card_access_crud as dbstore

from colorama import Fore, Back, Style
from datetime import datetime
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
parser.add_argument("-s", "--store-on-database", help='In this way will associate the Smart Card with the specific '
                                                      'user.', action="store_true")
parser.add_argument("-f", "--firstname", help='Firstname of the person to assign the Smart Card')
parser.add_argument("-l", "--lastname", help='Lastname of the person to assign the Smart Card')
parser.add_argument("-r", "--room-number", choices=['1', '2', '3', '4'], help='The room numer')

args = parser.parse_args()

# Get authentication key for Mifare Classic 1K Smart Card from program arguments
authentication_key = args.authentication_key

# Get Identity document number from program arguments
identification_number = args.document_id

# Get data of the user data
firstname = args.firstname
lastname = args.lastname
room_number = args.room_number
store_on_db = args.store_on_database


def print_version_info():
    """
    Print the version info about this python script.

    :return: void
    """
    art.tprint("Smart Card Init Tool")
    print("Version: %s" % version.__version__)
    print("Copyright (c) 2022 Antonio Musarra <antonio.musarra@gmail.com>")
    print("Antonio Musarra's Blog - https://www.dontesta.it")
    print("GitHub Project https://github.com/amusarra/smartcard-contactless-raspberry-pi")
    print("---\n")


def main():
    """
    The main entry point of this python script

    :return: void
    """
    print_version_info()

    error_on_card = False
    mifare_interface = mifare.MifareClassicInterface()
    mifare_interface.card_request_and_connect()

    uid = toHexString(mifare_interface.get_uid())
    reader = mifare_interface.get_reader()

    print(f"Smart Card Reader: {reader}")
    print(f"Card UID: {uid}\n")

    if mifare_interface.load_auth_key(toBytes(authentication_key)):
        if mifare_interface.authentication():
            print(f"{Fore.GREEN}Authentication successful{Style.RESET_ALL}\n")
            print(f"Get previous Identification Number {toASCIIString(mifare_interface.get_document_id())}")
            print(f"Try to store the new Identification Number {identification_number} into Smart Card...")

            result = mifare_interface.set_document_id(
                padd(toASCIIBytes(identification_number), 16, '00')
            )

            if result:
                print(f"Try to store the new Identification Number {identification_number} into Smart Card..."
                      f"{Fore.GREEN}[Stored]{Style.RESET_ALL}\n")
            else:
                error_on_card = True
                print(f"Error on store the Identification Number")
        else:
            error_on_card = True
            print("Authentication failed")
    else:
        error_on_card = True
        print("Load authentication key failed")

    mifare_interface.disconnect()

    # Check if store user data into MondoDB
    if store_on_db and not error_on_card:
        if firstname is None or lastname is None:
            print("The firstname and lastname must to be set")
            sys.exit(1)

        if room_number is None:
            print("The room numer must to be set")
            sys.exit(1)

        print(f"Starting store data into MongoDB ({firstname}, {lastname}, Room Number: {room_number})...")

        # 1. Connect to the db
        # 2. Check if document already exits
        # 3. Insert the document
        db = dbstore.SmartCardAccessCrud()

        search_filter = {"smartCardId": f"{uid}", "documentId": f"{identification_number}"}
        print(f"Searching entry on the MongoDB with filter {search_filter}...")

        document = db.read(search_filter)

        if len(document) == 0:
            print(f"Searching entry on the MongoDB with filter {search_filter}..."
                  f"{Fore.LIGHTYELLOW_EX}[Not Found]{Style.RESET_ALL}")
            new_document = dict(createDate=datetime.utcnow().isoformat() + "Z", firstname=f"{firstname}",
                                lastname=f"{lastname}", documentId=f"{identification_number}", smartCardEnabled="true",
                                smartCardId=f"{uid}", smartCardInitDate=datetime.utcnow().isoformat() + "Z",
                                roomNumber=int(room_number), countAccess=0)

            document_id = db.insert_data(new_document)
            print(f"Starting store data into MongoDB ({firstname}, {lastname}, Room Number: {room_number})..."
                  f"{Fore.GREEN}[Inserted with id: {document_id}]")
        else:
            print(f"Searching entry on the MongoDB with filter {search_filter}..."
                  f"{Fore.LIGHTYELLOW_EX}[Already exits]")

        print(f"{Fore.GREEN}\n-- Card initialized successfully and ready to use --")


if __name__ == "__main__":
    main()
