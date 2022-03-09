from setuptools import setup
from rpi import version

setup(
    name='smartcard-contactless-raspberry-pi',
    version=version.__version__,
    packages=['rpi', 'rpi.smartcard', 'rpi.smartcard.mifare', 'rpi.smartcard.mongodb', 'rpi.gpio'],
    install_requires=[
        'pyscard == 2.0.2',
        'art == 5.4',
        'pidfile == 0.1.1',
        'pid == 3.0.4',
        'pymongo == 4.0.1',
        'colorama == 0.4.4',
        'RPi.GPIO == 0.7.1',
        'fake - rpi == 0.7.1'
    ],
    url='https://www.dontesta.it',
    license='MIT',
    author='Antonio Musarra',
    author_email='antonio.musarra@gmail.com',
    description='Smart Card Contactless Raspberry Pi sample project',
)
