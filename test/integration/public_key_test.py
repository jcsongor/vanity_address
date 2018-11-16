from unittest import TestCase

from bitcoin_vanity.private_key import PrivateKey
from bitcoin_vanity.public_key import PublicKey


class PublicKeyTest(TestCase):
    def setUp(self):
        """see http://gobittest.appspot.com/Address for test values"""
        self._public_key = PublicKey(PrivateKey(12345))
        self._address = b'1Fy668EHkFwsrBQJfZsXYVgsGzKDaZhUEj'
        self._ecdsa_x = 0xF01D6B9018AB421DD410404CB869072065522BF85734008F105CF385A023A80F
        self._ecdsa_y = 0x0EBA29D0F0C5408ED681984DC525982ABEFCCD9F7FF01DD26DA4999CF3F6A295

    def test_point_returns_the_correct_x_and_y_values(self):
        point = self._public_key.point()

        self.assertEqual(point.x, self._ecdsa_x)
        self.assertEqual(point.y, self._ecdsa_y)

    def test_get_address_returns_the_correct_address_in_wif_format(self):
        address = self._public_key.get_address()

        self.assertEqual(address, self._address)
