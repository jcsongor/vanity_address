
[![Build Status](https://travis-ci.org/jcsongor/bitcoin_vanity.svg?branch=master)](https://travis-ci.org/jcsongor/bitcoin_vanity)
[![Coverage Status](https://coveralls.io/repos/github/jcsongor/bitcoin_vanity/badge.svg)](https://coveralls.io/github/jcsongor/bitcoin_vanity)

## Bitcoin vanity address generator

Generate bitcoin vanity addresses matched by an arbitrary callback.

## Installation
```bash
git clone https://github.com/jcsongor/bitcoin_vanity.git
cd bitcoin_vanity
pip install .

```

## Example usage
```python
# Generate an address
vanity_address = VanityAddressGenerator.generate_one(callback=callback)

# Generate multiple addresses
addresses = []
for address in VanityAddressGenerator.generate(callback=callback):
    addresses.append(address)
    if len(addresses) >= 5:
        break
```
