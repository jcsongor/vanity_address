from unittest import TestCase

from vanity_address.private_key import PrivateKey


class PrivateKeyTest(TestCase):
    def setUp(self):
        """see http://gobittest.appspot.com/PrivateKey for test values"""
        self._private_key = PrivateKey(12345)
        self._address = b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb'

    def test_int_returns_the_private_key_as_an_integer(self):
        self.assertEqual(int(self._private_key), 12345)

    def test_bytes_returns_the_private_key_in_wif_format(self):
        wif = bytes(self._private_key)

        self.assertEqual(wif, self._address)

    def test_str_returns_the_private_key_in_wif_format(self):
        wif = str(self._private_key)

        self.assertEqual(wif, self._address.decode('utf-8'))
