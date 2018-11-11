from unittest import TestCase
from unittest.mock import patch

from bitcoin_vanity.lib.hash import sha256, ripemd160


class Sha256Test(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._bytes = b'\x1a+<'
        self._sha256_result = 'f26c9c06a82db27233b98a2b1c5a778c987613f7589ef1fa04c39fe3f6e30e3b'

    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_sha256_calls_unhexlify(self, unhexlify):
        unhexlify.return_value = self._bytes

        sha256(self._hex_str)

        unhexlify.assert_called_once_with(self._hex_str)

    @patch('bitcoin_vanity.lib.hash.hashlib.sha256')
    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_sha256_calls_hashlib_sha256(self, unhexlify, hashlib_sha256):
        unhexlify.return_value = self._bytes

        sha256(self._hex_str)

        hashlib_sha256.assert_any_call(self._bytes)

    @patch('bitcoin_vanity.lib.hash.hashlib.sha256')
    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_sha256_gets_sha_hexdigest(self, unhexlify, hashlib_sha256):
        unhexlify.return_value = self._bytes
        hashlib_sha256.return_value.hexdigest.return_value = self._sha256_result

        sha256(self._hex_str)

        hashlib_sha256.return_value.hexdigest.assert_called_once()

    @patch('bitcoin_vanity.lib.hash.hashlib.sha256')
    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_sha256_returns_the_sha_hexdigest(self, unhexlify, hashlib_sha256):
        unhexlify.return_value = self._bytes
        hashlib_sha256.return_value.hexdigest.return_value = self._sha256_result

        result = sha256(self._hex_str)

        self.assertEqual(result, self._sha256_result)

    def test_sha256_returns_the_correct_hash(self):
        result = sha256(self._hex_str)

        self.assertEqual(result, self._sha256_result)


class RipemdTest(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._bytes = b'\x1a+<'
        self._ripemd160_result = '2885f0092763dc3b0761e43cb64a9de1af9a16bb'

    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_ripemd160_calls_unhexlify(self, unhexlify):
        unhexlify.return_value = self._bytes

        ripemd160(self._hex_str)

        unhexlify.assert_called_once_with(self._hex_str)

    @patch('bitcoin_vanity.lib.hash.hashlib')
    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_ripemd160_calls_hashlib_ripemd160(self, unhexlify, hashlib):
        unhexlify.return_value = self._bytes

        ripemd160(self._hex_str)

        hashlib.new.assert_any_call('ripemd160', self._bytes)

    @patch('bitcoin_vanity.lib.hash.hashlib')
    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_ripemd160_gets_sha_hexdigest(self, unhexlify, hashlib):
        unhexlify.return_value = self._bytes
        hashlib.new.return_value.hexdigest.return_value = self._ripemd160_result

        ripemd160(self._hex_str)

        hashlib.new.return_value.hexdigest.assert_called_once()

    @patch('bitcoin_vanity.lib.hash.hashlib')
    @patch('bitcoin_vanity.lib.hash.unhexlify')
    def test_ripemd160_returns_the_sha_hexdigest(self, unhexlify, hashlib):
        unhexlify.return_value = self._bytes
        hashlib.new.return_value.hexdigest.return_value = self._ripemd160_result

        result = ripemd160(self._hex_str)

        self.assertEqual(result, self._ripemd160_result)

    def test_ripemd160_returns_the_correct_hash(self):
        result = ripemd160(self._hex_str)

        self.assertEqual(result, self._ripemd160_result)
