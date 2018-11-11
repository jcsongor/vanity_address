from unittest import TestCase
from unittest.mock import patch

from bitcoin_vanity.private_key import PrivateKey
from bitcoin_vanity.public_key import PublicKey


class PublicKeyTest(TestCase):
    def setUp(self):
        """see http://gobittest.appspot.com/Address for test values"""
        self._public_key = PublicKey(PrivateKey(12345))
        self._ecdsa_x = 0xF01D6B9018AB421DD410404CB869072065522BF85734008F105CF385A023A80F
        self._ecdsa_y = 0xEBA29D0F0C5408ED681984DC525982ABEFCCD9F7FF01DD26DA4999CF3F6A295
        self._public_key_ecdsa = '04F01D6B9018AB421DD410404CB869072065522BF85734008F105CF385A023A80F0EBA29D0F0C5408ED681984DC525982ABEFCCD9F7FF01DD26DA4999CF3F6A295'
        self._hash160_of_public_key = 'a42d4d68affbb92a4a733df0d5bf9375456921e5'
        self._hash160_with_network_prefix = '00a42d4d68affbb92a4a733df0d5bf9375456921e5'
        self._hash160_with_testnet_prefix = '6fa42d4d68affbb92a4a733df0d5bf9375456921e5'
        self._hash256_of_hash160 = 'ea6c8ec822a1e401228ebe4aeed5118f8049fe88cca6bd29f3546d4a1a69b905'
        self._hash160_with_checksum = '00a42d4d68affbb92a4a733df0d5bf9375456921e5ea6c8ec8'
        self._address = b'1Fy668EHkFwsrBQJfZsXYVgsGzKDaZhUEj'

    def test_point_returns_the_correct_x_and_y_values(self):
        point = self._public_key.point()

        self.assertEqual(point.x, self._ecdsa_x)
        self.assertEqual(point.y, self._ecdsa_y)

    @patch('bitcoin_vanity.public_key.hash160')
    def test_get_address_hashes_the_public_key_with_hash160(self, hash160):
        hash160.return_value = self._hash160_of_public_key

        self._public_key.get_address()

        hash160.assert_called_once_with(self._public_key_ecdsa)

    @patch('bitcoin_vanity.public_key.hash256')
    @patch('bitcoin_vanity.public_key.hash160')
    def test_get_address_hashes_the_ripemd_of_the_sha_of_the_public_key_with_hash256(self, hash160, hash256):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        self._public_key.get_address()

        hash256.assert_called_once_with(self._hash160_with_network_prefix)

    @patch('bitcoin_vanity.public_key.base58encode')
    @patch('bitcoin_vanity.public_key.hash256')
    @patch('bitcoin_vanity.public_key.hash160')
    def test_get_address_base58encodes_the_ripemd_and_the_checksum(self, hash160, hash256, base58encode):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        self._public_key.get_address()

        base58encode.assert_called_once_with(self._hash160_with_checksum)

    @patch('bitcoin_vanity.public_key.base58encode')
    def test_get_address_returns_the_base58encoded_address(self, base58encode):
        base58encode.return_value = self._address

        address = self._public_key.get_address()

        self.assertEqual(address, self._address)

    @patch('bitcoin_vanity.public_key.hash256')
    @patch('bitcoin_vanity.public_key.hash160')
    def test_get_address_prepends_the_correct_prefix_for_testnet_addresses(self, hash160, hash256):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        public_key = PublicKey(PrivateKey(12345, testnet=True))
        public_key.get_address()

        hash256.assert_called_once_with(self._hash160_with_testnet_prefix)

    def test_get_address_returns_the_correct_address_in_wif_format(self):
        address = self._public_key.get_address()

        self.assertEqual(address, self._address)


