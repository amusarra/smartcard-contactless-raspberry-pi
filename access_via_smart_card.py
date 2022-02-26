#!/usr/bin/env python
# coding=utf-8

"""
Python scripts for Access control via Mifare Classic 1K Smart Card.

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

from pid.decorator import pidfile
from rpi import version
from rpi.gpio.manage_relay import ManageRelay
from time import sleep
from smartcard.CardMonitoring import CardMonitor
from smartcard.util import toBytes


# Setup parser argument
parser = argparse.ArgumentParser(description='Smart Card Access Control tool.\n This tool is valid for MIFARE Classic '
                                             '1K cards. It must be used to access to the system. '
                                             'Once verified that the card is valid, the system will activate the relay'
                                             ' to open the door corresponding to the assigned room.')
parser.add_argument("-a", "--authentication-key", help='Authentication Key of Mifare Classic 1K.The authentication '
                                                       'keys are used to authenticate the particular sector of the '
                                                       'MIFARE Classic 1K memory card. Volatile authentication key '
                                                       'location is provided.', required=True)
args = parser.parse_args()

# Get authentication key for Mifare Classic 1K Smart Card from program arguments
authentication_key = args.authentication_key


def print_version_info():
    """
    Print the version info about this python script.

    :return: void
    """
    art.tprint("Smart Card Access Tool")
    print("Version: %s" % version.__version__)
    print("Copyright (c) 2022 Antonio Musarra <antonio.musarra@gmail.com>")
    print("Antonio Musarra's Blog - https://www.dontesta.it")
    print("GitHub Project https://github.com/amusarra/smartcard-contactless-raspberry-pi")
    print("---\n")


@pidfile()
def main():
    """
    The main entry point of this python script

    :return: void
    """

    try:
        print_version_info()

        # Initialize the GPIO for the relays module
        ManageRelay.init_gpio()

        # Instantiate the Mifare Classic Interface Object
        mifare_interface_observer = mifare.MifareClassicInterface(toBytes(authentication_key))

        print("Insert or remove a Smart Card in the reader.")
        print("Press ctrl+c to exit")
        print("")

        # Add Card Monitor Observer to the Mifare Classic Interface
        card_monitor = CardMonitor()
        card_monitor.addObserver(mifare_interface_observer)

        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Goodbye")

    finally:
        # don't forget to remove observer, or the
        # monitor will poll forever...
        card_monitor.deleteObserver(mifare_interface_observer)

        # Cleanup the GPIO resources
        ManageRelay.cleanup()


if __name__ == "__main__":
    main()
