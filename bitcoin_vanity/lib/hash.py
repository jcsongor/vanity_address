import hashlib
from binascii import unhexlify


def hash256(hexstr: str) -> str:
    return sha256(sha256(hexstr))


def sha256(hexstr: str) -> str:
    return hashlib.sha256(unhexlify(hexstr)).hexdigest()


def ripemd160(hexstr: str) -> str:
    return hashlib.new('ripemd160', unhexlify(hexstr)).hexdigest()
