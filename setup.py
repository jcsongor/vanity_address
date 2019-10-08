from setuptools import setup

setup(
    name='vanity_address',
    version='0.1.4',
    description='Bitcoin vanity address miner',
    url='https://github.com/jcsongor/vanity_address',
    author='Jozsa Csongor',
    author_email='jozsa.csongor@gmail.com',
    license='MIT',
    long_description='Generate bitcoin vanity addresses matched by an arbitrary callback.',
    packages= ['vanity_address', 'vanity_address.lib'],
    entry_points={
        'console_scripts': ['vanityaddr=vanity_address.generate:main'],
    },
    install_requires=[
        'ecdsa==0.13.3',
        'base58==1.0.2',
    ],
    extras_require={
        'dev': [
            'coverage==4.5.2',
            'coveralls==1.5.1',
        ]
    },
    zip_safe=False
)
