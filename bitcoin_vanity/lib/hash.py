import hashlib
from binascii import unhexlify


def sha256(hexstr: str) -> str:
    return hashlib.sha256(unhexlify(hexstr)).hexdigest()


def ripemd160(hexstr: str) -> str:
    return hashlib.new('ripemd160', unhexlify(hexstr)).hexdigest()
