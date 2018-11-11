from collections import namedtuple
from ecdsa.ellipticcurve import CurveFp, Point

from bitcoin_vanity.lib.encode import base58encode, hex_string
from bitcoin_vanity.lib.hash import hash256, hash160
from bitcoin_vanity.private_key import PrivateKey


class PublicKey:
    _p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    _r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    _b = 0x0000000000000000000000000000000000000000000000000000000000000007
    _a = 0x0000000000000000000000000000000000000000000000000000000000000000
    _Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    _Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    _curve = CurveFp(_p, _a, _b)
    _generator = Point(_curve, _Gx, _Gy, _r)

    def __init__(self, private_key: PrivateKey):
        self._point = self._generator * int(private_key)
        self._testnet = private_key.is_testnet_key()

    def point(self) -> Point:
        Point = namedtuple('Point', ['x', 'y'])
        return Point(self._point.x(), self._point.y())

    def get_address(self) -> bytes:
        key = self._get_key_as_hex_string()
        hash = self._get_network_prefix() + hash160(key)
        checksum = self._calculate_checksum(hash)
        return base58encode(hash + checksum)

    def _get_key_as_hex_string(self) -> str:
        #TODO: support compressed public keys
        return '04' + hex_string(self._point.x()) + hex_string(self._point.y())

    def _get_network_prefix(self) -> str:
        return '6f' if self._testnet else '00'

    def _calculate_checksum(self, hex_str: str) -> str:
        return hash256(hex_str)[:8]
