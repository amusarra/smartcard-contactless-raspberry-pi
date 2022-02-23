from setuptools import setup

setup(
    name='smartcard-contactless-raspberry-pi',
    packages=['rpi', 'rpi.smartcard', 'rpi.smartcard.mifare', 'rpi.smartcard.mongodb'],
    url='https://www.dontesta.it',
    license='MIT',
    author='Antonio Musarra',
    author_email='antonio.musarra@gmail.com',
    description='Smart Card Contactless Raspberry Pi sample project',
    use_scm_version=True,
    setup_requires=['setuptools_scm']
)
