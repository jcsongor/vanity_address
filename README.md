
[![Build Status](https://travis-ci.org/jcsongor/bitcoin_vanity.svg?branch=master)](https://travis-ci.org/jcsongor/bitcoin_vanity)
[![Coverage Status](https://coveralls.io/repos/github/jcsongor/bitcoin_vanity/badge.svg)](https://coveralls.io/github/jcsongor/bitcoin_vanity)

## Bitcoin vanity address generator

Generate bitcoin addresses matching a given pattern.
Vanity addresses can be used:
- to make spoofing your address more expensive
- to spoof other bitcoin addresses
- for the cool factor

## Installation
```bash
git clone https://github.com/jcsongor/bitcoin_vanity.git
cd bitcoin_vanity
pip install .

```

## Example usage
```python
import re

from bitcoin_vanity.vanity_address_generator import VanityAddressGenerator

vanity_address_generator = VanityAddressGenerator()
pattern_to_match = re.compile('.*12[AB].*')
private_key, address = vanity_address_generator.generate_matching_address(pattern_to_match)
print(int(private_key))
print(address)
```
## Example output
```bash
72318465368044105536176770127708051002996296243350562176598702416836806776103
b'12Bn8vSvBmU6HNdCranfVt7vxsnyNUkVKE'
```
