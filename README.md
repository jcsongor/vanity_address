
[![Build Status](https://travis-ci.org/jcsongor/vanity_address.svg?branch=master)](https://travis-ci.org/jcsongor/vanity_address)
[![Coverage Status](https://coveralls.io/repos/github/jcsongor/vanity_address/badge.svg)](https://coveralls.io/github/jcsongor/vanity_address)

## Bitcoin vanity address generator

Generate bitcoin vanity addresses matched by an arbitrary callback.

## Installation
### Using from PyPI
```bash
pip install vanity_address
```

### Install the latest version from github
```bash
git clone https://github.com/jcsongor/vanity_address.git
cd vanity_address
pip install .
```

## Usage
### Using the command line interface

```bash
$ vanityaddr PATTERN 
```

### Using the python module
#### Generate an address
```python
def callback(address):
    return address.startswith(b'11')
    
vanity_address = VanityAddressGenerator.generate_one(callback=callback)
```
#### Generate multiple addresses
```python
addresses = []
for address in VanityAddressGenerator.generate(callback=callback):
    addresses.append(address)
    if len(addresses) >= 5:
        break
```

