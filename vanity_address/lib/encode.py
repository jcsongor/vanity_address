from base58 import b58encode
from binascii import unhexlify


def base58encode(to_encode: str) -> bytes:
    return b58encode(unhexlify(to_encode))


def hex_string(number: int, length: int = 64):
    format_string = '%%0%dX' % length
    return format_string % number
