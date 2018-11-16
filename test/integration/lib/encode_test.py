from unittest import TestCase

from bitcoin_vanity.lib.encode import base58encode


class Base58EncodeTest(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._b58encode_result = b'9np3'

    def test_base58encode_returns_the_correct_hash(self):
        result = base58encode(self._hex_str)

        self.assertEqual(result, self._b58encode_result)
