from unittest import TestCase
from unittest.mock import patch, MagicMock

from vanity_address.coins.public_key import PublicKey


class PublicKeyTest(TestCase):
    def setUp(self):
        """see http://gobittest.appspot.com/Address for test values"""
        private_key = self._mock_private_key(12345)
        self._public_key = PublicKey(private_key)
        self._public_key_ecdsa = '04F01D6B9018AB421DD410404CB869072065522BF85734008F105CF385A023A80F0EBA29D0F0C5408ED681984DC525982ABEFCCD9F7FF01DD26DA4999CF3F6A295'
        self._hash160_of_public_key = 'a42d4d68affbb92a4a733df0d5bf9375456921e5'
        self._hash160_with_network_prefix = '00a42d4d68affbb92a4a733df0d5bf9375456921e5'
        self._hash160_with_testnet_prefix = '6fa42d4d68affbb92a4a733df0d5bf9375456921e5'
        self._hash256_of_hash160 = 'ea6c8ec822a1e401228ebe4aeed5118f8049fe88cca6bd29f3546d4a1a69b905'
        self._hash160_with_checksum = '00a42d4d68affbb92a4a733df0d5bf9375456921e5ea6c8ec8'
        self._address = b'1Fy668EHkFwsrBQJfZsXYVgsGzKDaZhUEj'
        self._compressed_public_key_ecdsa_odd = '03F01D6B9018AB421DD410404CB869072065522BF85734008F105CF385A023A80F'
        self._compressed_public_key_ecdsa_even = '021C96466679CF8831360B6AA09427E10ABD386C9168E8C6F2ACED993209B0AC08'

    @patch('vanity_address.coins.public_key.hash160')
    def test_get_address_hashes_the_public_key_with_hash160(self, hash160):
        hash160.return_value = self._hash160_of_public_key

        self._public_key.get_address()

        hash160.assert_called_once_with(self._public_key_ecdsa)

    @patch('vanity_address.coins.public_key.hash256')
    @patch('vanity_address.coins.public_key.hash160')
    def test_get_address_hashes_the_ripemd_of_the_sha_of_the_public_key_with_hash256(self, hash160, hash256):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        self._public_key.get_address()

        hash256.assert_called_once_with(self._hash160_with_network_prefix)

    @patch('vanity_address.coins.public_key.base58encode')
    @patch('vanity_address.coins.public_key.hash256')
    @patch('vanity_address.coins.public_key.hash160')
    def test_get_address_base58encodes_the_ripemd_and_the_checksum(self, hash160, hash256, base58encode):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        self._public_key.get_address()

        base58encode.assert_called_once_with(self._hash160_with_checksum)

    @patch('vanity_address.coins.public_key.base58encode')
    def test_get_address_returns_the_base58encoded_address(self, base58encode):
        base58encode.return_value = self._address

        address = self._public_key.get_address()

        self.assertEqual(address, self._address)

    @patch('vanity_address.coins.public_key.hash256')
    @patch('vanity_address.coins.public_key.hash160')
    def test_get_address_prepends_the_correct_prefix_for_testnet_addresses(self, hash160, hash256):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160
        private_key = self._mock_private_key(12344, testnet=True)
        public_key = PublicKey(private_key)

        public_key.get_address()

        hash256.assert_called_once_with(self._hash160_with_testnet_prefix)

    @patch('vanity_address.coins.public_key.hash160')
    def test_get_address_prepends_the_correct_prefix_for_odd_compressed_keys(self, hash160):
        hash160.return_value = self._hash160_of_public_key
        private_key = self._mock_private_key(12345, compressed=True)
        public_key = PublicKey(private_key)

        public_key.get_address()

        hash160.assert_called_once_with(self._compressed_public_key_ecdsa_odd)

    @patch('vanity_address.coins.public_key.hash160')
    def test_get_address_prepends_the_correct_prefix_for_even_compressed_keys(self, hash160):
        hash160.return_value = self._hash160_of_public_key
        private_key = self._mock_private_key(12344, compressed=True)
        public_key = PublicKey(private_key)

        public_key.get_address()

        hash160.assert_called_once_with(self._compressed_public_key_ecdsa_even)

    def _mock_private_key(self, int_value, compressed=False, testnet=False):
        private_key = MagicMock()
        private_key.__int__.return_value = int_value
        private_key.is_compressed.return_value = compressed
        private_key.is_testnet_key.return_value = testnet
        return private_key

