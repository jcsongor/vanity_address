#!/usr/bin/env python
import re

from bitcoin_vanity.vanity_address_generator import VanityAddressGenerator

vanity_address_generator = VanityAddressGenerator()
pattern_to_match = re.compile('.*12[AB].*')
private_key, address = vanity_address_generator.generate_matching_address(pattern_to_match)
print(int(private_key))
print(address)
