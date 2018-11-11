from unittest import TestCase
from unittest.mock import patch

from bitcoin_vanity.lib.encode import base58encode, hex_string


class Base58EncodeTest(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._bytes = b'\x1a+<'
        self._b58encode_result = b'9np3'

    @patch('bitcoin_vanity.lib.encode.unhexlify')
    def test_base58encode_calls_unhexlify(self, unhexlify):
        unhexlify.return_value = self._bytes

        base58encode(self._hex_str)

        unhexlify.assert_called_once_with(self._hex_str)

    @patch('bitcoin_vanity.lib.encode.b58encode')
    @patch('bitcoin_vanity.lib.encode.unhexlify')
    def test_base58encode_calls_hashlib_base58encode(self, unhexlify, b58encode):
        unhexlify.return_value = self._bytes

        base58encode(self._hex_str)

        b58encode.assert_called_once_with(self._bytes)

    @patch('bitcoin_vanity.lib.encode.b58encode')
    @patch('bitcoin_vanity.lib.encode.unhexlify')
    def test_base58encode_returns_the_base58encoded_string(self, unhexlify, b58encode):
        unhexlify.return_value = self._bytes
        b58encode.return_value = self._b58encode_result

        result = base58encode(self._hex_str)

        self.assertEqual(result, self._b58encode_result)

    def test_base58encode_returns_the_correct_hash(self):
        result = base58encode(self._hex_str)

        self.assertEqual(result, self._b58encode_result)

class HexStringTest(TestCase):
    def setUp(self):
        self._int = 1715004
        self._hex_str = '1A2B3C'
        self._padded_hex_str = '00000000000000000000000000000000000000000000000000000000001A2B3C'

    def test_hex_string_returns_64_chars_long_string_by_default(self):
        result = hex_string(self._int)

        self.assertEqual(result, self._padded_hex_str)

    def test_hex_string_returns_the_correct_string(self):
        result = hex_string(self._int, 6)

        self.assertEqual(result, self._hex_str)
