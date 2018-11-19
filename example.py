#!/usr/bin/env python
import re

from bitcoin_vanity.vanity_address import Generator

vanity_address_generator = Generator()
pattern = re.compile('.*12[AB].*')
addresses = vanity_address_generator.generate(pattern, 3)

for private_key, address in addresses:
    print('Private key: %s' % int(private_key))
    print('Address: %s' % address)
