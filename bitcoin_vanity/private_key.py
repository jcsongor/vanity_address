from abc import ABC, abstractmethod

from secrets import randbits

from bitcoin_vanity.lib.encode import base58encode, hex_string
from bitcoin_vanity.lib.hash import sha256


class PrivateKey:
    TESTNET_PREFIX = 'ef'
    NORMAL_PREFIX = '80'
    COMPRESSED_SUFFIX = '01'

    def __init__(self, private_key: int, testnet=False, compressed=False):
        self._private_key = private_key
        self._testnet = testnet
        self._compressed = compressed

    def __int__(self):
        return self._private_key

    def __str__(self):
        return bytes(self).decode('utf-8')

    def __bytes__(self):
        """Returns the private key in Wallet Import Format. See https://en.bitcoin.it/wiki/Wallet_import_format"""
        return self._wif()

    def _wif(self):
        return base58encode(self._get_key_with_checksum())

    def _get_key_with_checksum(self):
        key = self._get_key_with_extra_bytes()
        return key + self._calculate_checksum(key)

    def _get_key_with_extra_bytes(self):
        return self._get_prefix() + hex_string(self._private_key) + self._get_suffix()

    def _get_prefix(self):
        return self.TESTNET_PREFIX if self._testnet else self.NORMAL_PREFIX

    def _get_suffix(self):
        return self.COMPRESSED_SUFFIX if self._compressed else ''

    def _calculate_checksum(self, key):
        hash = self._calculate_hash(key)
        return hash[:8]

    def _calculate_hash(self, key):
        hash1 = sha256(key)
        hash2 = sha256(hash1)
        return hash2


class RNG(ABC):
    @abstractmethod
    def randbits(self, bits: int) -> int:
        pass


class SecretsRNG(ABC):
    def randbits(self, bits: int) -> int:
        return randbits(bits)


class PrivateKeyGenerator:
    _biggest_valid_private_key = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140

    def __init__(self, rng: RNG):
        self._rng = rng

    def generate_private_key(self, testnet=False, compressed=False) -> PrivateKey:
        while True:
            candidate = self._rng.randbits(256)
            if self._is_valid(candidate):
                return PrivateKey(candidate, testnet=testnet, compressed=compressed)

    def _is_valid(self, private_key_candidate: int) -> bool:
        return private_key_candidate <= self._biggest_valid_private_key
