import re

from bitcoin_vanity.private_key import PrivateKeyGenerator, SecretsRNG
from bitcoin_vanity.public_key import PublicKey


class VanityAddressGenerator:
    def __init__(self):
        rng = SecretsRNG()
        self._private_key_generator = PrivateKeyGenerator(rng)

    def generate_matching_address(self, pattern: re) -> (str, str):
        while True:
            private_key, address = self._generate_candidate()
            if pattern.match(address) is not None:
                return private_key, address

    def _generate_candidate(self) -> (str, str):
        private_key = self._private_key_generator.generate_private_key()
        public_key = PublicKey(private_key)
        return private_key, str(public_key.get_address())
