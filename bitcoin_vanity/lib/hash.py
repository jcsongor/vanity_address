import hashlib
from binascii import unhexlify


def sha256(hexstr):
    return hashlib.sha256(unhexlify(hexstr)).hexdigest()


def ripemd160(hexstr):
    return hashlib.new('ripemd160', unhexlify(hexstr)).hexdigest()
