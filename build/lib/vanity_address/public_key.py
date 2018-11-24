from collections import namedtuple

from ecdsa.ellipticcurve import CurveFp, Point

from vanity_address.coins.private_key import PrivateKey
from vanity_address.lib.encode import base58encode, hex_string
from vanity_address.lib.hash import hash256, hash160


class PublicKey:
    _p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    _r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    _b = 0x0000000000000000000000000000000000000000000000000000000000000007
    _a = 0x0000000000000000000000000000000000000000000000000000000000000000
    _Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    _Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    _curve = CurveFp(_p, _a, _b)
    _generator = Point(_curve, _Gx, _Gy, _r)

    UNCOMPRESSED_PREFIX = '04'
    ODD_PREFIX = '03'
    EVEN_PREFIX = '02'
    TESTNET_PREFIX = '6f'
    MAINNET_PREFIX = '00'

    def __init__(self, private_key: PrivateKey):
        self._point = self._generator * int(private_key)
        self._testnet = private_key.is_testnet_key()
        self._compressed = private_key.is_compressed()

    def point(self) -> Point:
        Point = namedtuple('Point', ['x', 'y'])
        return Point(self._point.x(), self._point.y())

    def get_address(self) -> bytes:
        key = self._get_key_as_hex_string()
        hash = self._get_network_prefix() + hash160(key)
        checksum = self._calculate_checksum(hash)
        return base58encode(hash + checksum)

    def _get_key_as_hex_string(self) -> str:
        if self._compressed:
            return self._get_parity_prefix() + hex_string(self._point.x())
        return self.UNCOMPRESSED_PREFIX + hex_string(self._point.x()) + hex_string(self._point.y())

    def _get_parity_prefix(self):
        return self.ODD_PREFIX if self._point.y() % 2 == 1 else self.EVEN_PREFIX

    def _get_network_prefix(self) -> str:
        return self.TESTNET_PREFIX if self._testnet else self.MAINNET_PREFIX

    def _calculate_checksum(self, hex_str: str) -> str:
        return hash256(hex_str)[:8]
