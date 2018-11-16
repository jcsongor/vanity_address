from setuptools import setup

setup(
    name='bitcoin_vanity',
    version='0.1',
    description='Bitcoin vanity address miner',
    url='https://github.com/jcsongor/bitcoin_vanity',
    author='Jozsa Csongor',
    author_email='jozsa.csongor@gmail.com',
    license='MIT',
    packages=['bitcoin_vanity'],
    install_requires=[
        'ecdsa==0.13',
        'base58==1.0.2',
    ],
    extras_require={
        'dev': [
            'coverage',
        ]
    },
    zip_safe=False
)
