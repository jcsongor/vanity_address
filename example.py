#!/usr/bin/env python
from vanity_address.vanity_address import VanityAddressGenerator
from pprint import pprint

def callback(address):
    return address.startswith(b'11')

# Generate an address
address = VanityAddressGenerator.generate_one(callback=callback)

print("Address:\t{address.address}\nPrivate key:\t{address.private_key}".format(address=address))

# Generate multiple addresses
addresses = []
for address in VanityAddressGenerator.generate(callback=callback):
    addresses.append(address)
    if len(addresses) >= 5:
        break
pprint(addresses)
