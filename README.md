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
vanity_address = vanity_address_generator.generate_address(pattern_to_match)
print(vanity_address)
```
