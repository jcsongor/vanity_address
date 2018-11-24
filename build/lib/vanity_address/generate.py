#!/usr/bin/env python
import sys

from vanity_address.vanity_address import VanityAddressGenerator

def main():
    address = VanityAddressGenerator.generate_one(callback=lambda candidate: sys.argv[1] in str(candidate))

    print('Private key:\t%s' % address.private_key)
    print('Address:\t%s' % address.address.decode('utf-8'))
