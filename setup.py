from setuptools import setup
from rpi import version

setup(
    name='smartcard-contactless-raspberry-pi',
    version=version.__version__,
    packages=['rpi', 'rpi.smartcard', 'rpi.smartcard.mifare', 'rpi.smartcard.mongodb'],
    url='https://www.dontesta.it',
    license='MIT',
    author='Antonio Musarra',
    author_email='antonio.musarra@gmail.com',
    description='Smart Card Contactless Raspberry Pi sample project',
)
