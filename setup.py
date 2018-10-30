from setuptools import setup

setup(
    name='bitcoin_vanity',
    version='0.1',
    description='Bitcoin vanity address miner',
    url='http://github.com/jcsongor/bitcoin_vanity',
    author='Jozsa Csongor',
    author_email='jozsa.csongor@gmail.com',
    license='MIT',
    packages=['bitcoin_vanity'],
    install_requires=[
        'base58==1.0.2',
    ],
    zip_safe=False
)
