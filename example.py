#!/usr/bin/env python
from bitcoin_vanity.vanity_address import VanityAddressGenerator
from pprint import pprint

def callback(address):
    return address.startswith(b'11')

# Generate an address
vanity_address = VanityAddressGenerator.generate_one(callback=callback)

print("Address:\t{vanity_address.address}\nPrivate key:\t{vanity_address.private_key}".format(vanity_address=vanity_address))

# Generate multiple addresses
addresses = []
for address in VanityAddressGenerator.generate(callback=callback):
    addresses.append(address)
    if len(addresses) >= 5:
        break
pprint(addresses)
