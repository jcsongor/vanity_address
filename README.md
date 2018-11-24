
[![Build Status](https://travis-ci.org/jcsongor/vanity_address.svg?branch=master)](https://travis-ci.org/jcsongor/vanity_address)
[![Coverage Status](https://coveralls.io/repos/github/jcsongor/vanity_address/badge.svg)](https://coveralls.io/github/jcsongor/vanity_address)

## Bitcoin vanity address generator

Generate bitcoin vanity addresses matched by an arbitrary callback.

## Installation
### Using pip
```bash
pip install vanity_address
```

### Install from source
```bash
git clone https://github.com/jcsongor/vanity_address.git
cd vanity_address
pip install .

```

## Example usage
```python
def callback(address):
    return address.startswith(b'11')
    
# Generate an address
vanity_address = VanityAddressGenerator.generate_one(callback=callback)

# Generate multiple addresses
addresses = []
for address in VanityAddressGenerator.generate(callback=callback):
    addresses.append(address)
    if len(addresses) >= 5:
        break
```

## Using from the command line

```bash
$ vanityaddr PATTERN 

```
