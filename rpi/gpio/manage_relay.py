"""
Base class for interacting with Relay via GPIO

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

# Replace libraries by fake ones when in dev environment
try:
    import RPi.GPIO as GPIO

    dev_environment = False
except (ImportError, RuntimeError):
    dev_environment = True

if dev_environment:
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus  # Fake smbus (I2C)

    import RPi.GPIO as GPIO


class ManageRelay:
    """
    The Python interface to manage relay module via GPIO

    This class uses pyscard as a low-level interface to the NFC card,
    make sure your reader is compatible with this library.
    """

    def __init__(self):
        raise "This class is not instantiable. It only has static methods."

    # Dictionary of relationship between relay identification and BCM pin
    dict_relay_bcm = {
        1: 23,
        2: 24,
        3: 25,
        4: 16
    }

    @staticmethod
    def init_gpio():
        """
        Initialize the GPIO pin
        """

        # Setting GPIO mode to BCM (Broadcom)
        GPIO.setmode(GPIO.BCM)

        # Init GPIO pin
        for relay_id, bcm_value in ManageRelay.dict_relay_bcm.items():
            GPIO.setup(bcm_value, GPIO.OUT, initial=GPIO.HIGH)

    @staticmethod
    def activate_relay(relay_id):
        """
        Activate the relay by id

        :param relay_id: The integer that identify the relay
        :return: void
        """

        if 1 <= relay_id <= 4:
            GPIO.output(ManageRelay.dict_relay_bcm[relay_id], GPIO.LOW)

    @staticmethod
    def de_activate_relay(relay_id):
        """
        De-Activate the relay by id

        :param relay_id: The integer that identify the relay
        :return: void
        """

        if 1 <= relay_id <= 4:
            GPIO.output(ManageRelay.dict_relay_bcm[relay_id], GPIO.HIGH)

    @staticmethod
    def cleanup():
        """
        Clean the GPIO. Always remember to call this method when the GPIO resources are no longer needed.

        :return: void
        """
        GPIO.cleanup()
