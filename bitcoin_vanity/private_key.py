from abc import ABC, abstractmethod
from secrets import randbits
from hashlib import sha256
from base58 import b58encode
from binascii import unhexlify


class PrivateKey:
    def __init__(self, private_key: int, testnet=False, compressed=False):
        self._private_key = private_key
        self._testnet = testnet
        self._compressed = compressed

    def __int__(self):
        return self._private_key

    def __str__(self):
        return bytes(self).decode('utf-8')

    def __bytes__(self):
        return self._wif()

    def _wif(self):
        key = self._get_key_with_extra_bytes()
        checksum = self._calculate_checksum(key)
        return b58encode(unhexlify(key + checksum))

    def _get_key_with_extra_bytes(self):
        return self._get_prefix() + self._get_key_as_hex_string() + self._get_suffix()

    def _get_key_as_hex_string(self):
        return '%064X' % self._private_key

    def _get_prefix(self):
        return 'ef' if self._testnet else '80'

    def _get_suffix(self):
        return '01' if self._compressed else ''

    def _calculate_checksum(self, key):
        hash = self._calculate_hash(key)
        return hash[:8]

    def _calculate_hash(self, key):
        hash1 = sha256(unhexlify(key)).hexdigest()
        hash2 = sha256(unhexlify(hash1)).hexdigest()
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

    def generate_private_key(self) -> int:
        while True:
            candidate = self._rng.randbits(256)
            if self._is_valid(candidate):
                return candidate

    def _is_valid(self, private_key_candidate: int) -> bool:
        return private_key_candidate <= self._biggest_valid_private_key
