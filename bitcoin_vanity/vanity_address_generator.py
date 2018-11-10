import re

from bitcoin_vanity.private_key import PrivateKeyGenerator, SecretsRNG
from bitcoin_vanity.public_key import PublicKey


class VanityAddressGenerator:
    def __init__(self):
        rng = SecretsRNG()
        self._private_key_generator = PrivateKeyGenerator(rng)

    def generate_address(self, pattern: re) -> str:
        while True:
            candidate = self._generate_candidate()
            if pattern.match(candidate) is not None:
                return candidate

    def _generate_candidate(self) -> str:
        private_key = self._private_key_generator.generate_private_key()
        public_key = PublicKey(private_key)
        return str(public_key.get_address())
