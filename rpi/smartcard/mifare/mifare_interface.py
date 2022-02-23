"""
Base class for interacting with Mifare Classic 1K Smart Cards

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

import sys
from rpi import version
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.util import toBytes

__author__ = "Antonio Musarra"
__copyright__ = "Copyright (c) 2022 Antonio Musarra (Antonio Musarra's Blog - https://www.dontesta.it)"
__credits__ = ["Antonio Musarra"]
__version__ = version.__version__
__license__ = "MIT"
__maintainer__ = "Antonio Musarra"
__email__ = "antonio.musarra@gmail.com"
__status__ = "Development"


class MifareClassicInterface:
    """
    The Python interface to initialize data on Mifare Classic 1K
    Smart Card

    This class uses pyscard as a low-level interface to the NFC card,
    make sure your reader is compatible with this library.
    """

    def __init__(self):
        """
        Initialize and connect to the Smart Card
        """

        # Mifare Classic 1k ATR
        self.MIFARE_CLASSIC_1K_ATR = "3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A"

        # Define the card type and initialize the Card Request
        self.__card_type = ATRCardType(toBytes(self.MIFARE_CLASSIC_1K_ATR))
        self.__card_service = None
        self.__card_request = None

        # To checking if authentication process, it's fine
        self.__authenticated = False

    def authentication(self):
        """
        This method uses the keys stored in the reader to do authentication with the MIFARE 1K/4K card (PICC).
        Two types of authentication keys are used: TYPE_A and TYPE_B.

        For MIFARE Classic 1K Card, it has totally 16 sectors and each sector consists of 4
        consecutive blocks. E.g. Sector 00h consists of Blocks {00h, 01h, 02h and 03h};
        Sector 01h consists of Blocks {04h, 05h, 06h and 07h}; the last sector 0F consists of Blocks
        {3Ch, 3Dh, 3Eh and 3Fh}. Once the authentication is done successfully, there is no need to do the
        authentication again if the blocks to be accessed belong to the same sector.
        Please refer to the MIFARE Classic 1K/4K specification for more details

        Load Authentication Keys APDU Format (10 bytes)
        |--------------------------------------------------------------------------|
        | Command        | Class | INS | P1  | P2  | Lc  | Data In                 |
        |--------------------------------------------------------------------------|
        | Authentication | FFh   | 86h | 00h | 00h | 05h | Authenticate Data Bytes |
        |--------------------------------------------------------------------------|

        Authenticate Data Bytes (5 bytes)
        |--------------------------------------------------------------------------|
        | Byte 1       | Byte 2 | Byte 3        | Byte 4   | Byte 5                |
        |--------------------------------------------------------------------------|
        | Version 01h | 00h     | Block Number | Key Type | Key Number             |
        |--------------------------------------------------------------------------|

        Where:
            Block Number:   1 byte. This is the memory block to be authenticated.
            Key Type:       1 byte
                            60h = Key is used as a TYPE A key for authentication.
                            61h = Key is used as a TYPE B key for authentication.
            Key Number      1 byte
                            00h ~ 01h = Key Location.

        :return: True if it's ok False otherwise
        """

        # APDU to authentication
        apdu_authentication = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, 0x01, 0x60, 0x00]

        # Success   sw1=90 sw2=00h The operation completed successfully
        # Error     sw1=63 sw2=00h The operation failed.
        data, sw1, sw2 = self.__card_service.connection.transmit(apdu_authentication)

        if sw1 == 0x90:
            self.__authenticated = True
            return True
        else:
            return False

    def card_request_and_connect(self):
        """
        Make a Card Request and establishes a connection

        :except: In case of an exception on the connection the program will terminate.
        :return: void
        """
        self.__card_request = CardRequest(timeout=3, cardType=self.__card_type)

        # Wait for the card
        print('Waiting for the Mifare Classic 1K...')

        try:
            self.__card_service = self.__card_request.waitforcard()
        except CardRequestTimeoutException:
            print('Card not found, exiting')
            sys.exit(1)

        # Connect to the card if found
        self.__card_service.connection.connect()

    def disconnect(self):
        """
        Disconnect to the Smart Card

        :return: void
        """

        self.__card_service.connection.disconnect()

    def get_atr(self):
        """
        Return the ATR of the Smart Card

        :return: The ATR of the Smart Card
        """
        return self.__card_service.connection.getATR()

    def get_document_id(self):
        """
        Send APDU for getting the identification number of the identification document (example: identity card,
        driving license, social security number, passport number) of the person to whom the card is delivered.

        :return: The identification number of the identification document
        """

        # APDU to read the 16 bytes from the binary block 04h
        apdu_document_id = [0xFF, 0xB0, 0x00, 0x01, 0x10]

        # Success   sw1=90 sw2=00h The operation completed successfully
        # Error     sw1=63 sw2=00h The operation failed.
        data, sw1, sw2 = self.__card_service.connection.transmit(apdu_document_id)

        if sw1 == 0x90:
            return data
        else:
            print("Error on getting the UID")

    def get_reader(self):
        """
        Return the information about the Smart Card Reader

        :return: The information about the Smart Card Reader
        """

        return self.__card_service.connection.getReader()

    def get_uid(self):
        """
        Send APDU for getting the card UID

        :return: The UID of the Mifare Classic 1K card
        """

        apdu = [0xFF, 0xCA, 0x00, 0x00, 0x04]

        # Success   sw1=90 sw2=00h The operation completed successfully
        # Error     sw1=63 sw2=00h The operation failed.
        # Error     sw1=6A sw2=81h Function not supported
        data, sw1, sw2 = self.__card_service.connection.transmit(apdu)

        if sw1 == 0x90:
            return data
        else:
            print("Error on getting the UID")

    def load_auth_key(self, key):
        """
        This method loads the authentication keys into the reader. The authentication keys are used to
        authenticate the particular sector of the MIFARE Classic 1K/4K memory card.
        Volatile authentication key location is provided.

        Load Authentication Keys APDU Format (11 bytes)
        |-------------------------------------------------------------------------------------------|
        | Command                   | Class | INS | P1            | P2         | Lc  | Data In      |
        |-------------------------------------------------------------------------------------------|
        | Load Authentication Keys | FFh   | 82h | Key Structure | Key Number | 06h | Key (6 bytes) |
        |-------------------------------------------------------------------------------------------|

        Where:
            Key Structure   1 byte.
                            00h = Key is loaded into the reader volatile memory.
                            Other = Reserved.
            Key Number      1 byte.
                            00h ~ 01h = Key Location. The keys will disappear once the reader is
                            disconnected from the PC.
            Key 6 bytes.
                            The key value loaded into the reader. e.g., {FF FF FF FF FF FFh}

        :param key: The Load Authentication Key (es: 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF). The length must be of 6 bytes
        :return: True if the load authentication keys it's ok false otherwise
        """

        # APDU to load the authentication keys into the reader
        apdu_load_key = [0xFF, 0x82, 0x00, 0x00, 0x06] + key

        # Success   sw1=90 sw2=00h The operation completed successfully
        # Error     sw1=63 sw2=00h The operation failed.
        data, sw1, sw2 = self.__card_service.connection.transmit(apdu_load_key)

        if sw1 == 0x90:
            return True
        else:
            return False

    def set_document_id(self, document_id):
        """
        Send APDU for setting (store) the identification number of the identification document (example: identity card,
        driving license, social security number, passport number) of the person to whom the card is delivered.

        :return: True if store it's ok False otherwise
        """

        # APDU to read the 16 bytes from the binary block 04h
        apdu_document_id = [0xFF, 0xD6, 0x00, 0x01, 0x10] + document_id

        # Success   sw1=90 sw2=00h The operation completed successfully
        # Error     sw1=63 sw2=00h The operation failed.
        data, sw1, sw2 = self.__card_service.connection.transmit(apdu_document_id)

        if sw1 == 0x90:
            return True
        else:
            return False
