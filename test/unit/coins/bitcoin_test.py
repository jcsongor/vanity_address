from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from vanity_address.coins.bitcoin import PrivateKeyGenerator, SecretsRNG, PrivateKey, PublicKey




@patch('vanity_address.coins.bitcoin.randbits')
class SecretsRNGTest(TestCase):
    def setUp(self):
        self._rng = SecretsRNG()

    def test_randbits_generates_a_random_integer(self, secrets_randbits):
        self._rng.randbits(128)

        secrets_randbits.assert_called_once_with(128)

    def test_randbits_returns_with_the_random_integer(self, secrets_randbits):
        secrets_randbits.return_value = 12345

        result = self._rng.randbits(128)

        self.assertEqual(result, 12345)


class PrivateKeyGeneratorTest(TestCase):
    def setUp(self):
        self._rng = MagicMock()
        self._valid_private_keys = [0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140, 1, 2, 3]
        self._rng.randbits.side_effect = [
                                             0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
                                             0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
                                         ] + self._valid_private_keys

        self._private_key_generator = PrivateKeyGenerator(self._rng)

    def test_generate_private_key_generates_256_bit_integers_until_it_finds_a_valid_key(self):
        self._private_key_generator.generate_private_key()

        self._rng.randbits.assert_has_calls([call(256), call(256), call(256)])

    def test_generate_private_key_returns_the_first_valid_key_it_finds(self):
        private_key = self._private_key_generator.generate_private_key()

        self.assertEqual(int(private_key), self._valid_private_keys[0]),

    @patch('vanity_address.coins.bitcoin.PrivateKey')
    def test_generate_can_generate_compressed_and_test_network_keys(self, private_key):
        self._private_key_generator.generate_private_key()
        self._private_key_generator.generate_private_key(compressed=True)
        self._private_key_generator.generate_private_key(testnet=True)
        self._private_key_generator.generate_private_key(testnet=True, compressed=True)

        private_key.assert_has_calls([
            call(self._valid_private_keys[0], testnet=False, compressed=False),
            call(self._valid_private_keys[1], testnet=False, compressed=True),
            call(self._valid_private_keys[2], testnet=True, compressed=False),
            call(self._valid_private_keys[3], testnet=True, compressed=True),
        ])


class PrivateKeyTest(TestCase):
    def setUp(self):
        """see http://gobittest.appspot.com/PrivateKey for test values"""
        self._private_key = PrivateKey(12345)
        self._private_key_with_prefix = '800000000000000000000000000000000000000000000000000000000000003039'
        self._testnet_private_key = 'ef0000000000000000000000000000000000000000000000000000000000003039'
        self._private_key_with_checksum = '800000000000000000000000000000000000000000000000000000000000003039180D8C2E'
        self._compressed_private_key = '80000000000000000000000000000000000000000000000000000000000000303901'
        self._first_hash = '5976C6B48D1DC862AEB0C8BC3126A2751CC48E36737009DF688A9F0787A4624A'
        self._second_hash = '180D8C2E6CBBFFCE35A0BB172CBAC966FD9AC8B7F5CB9D70C3DC8C70B90AC88C'
        self._address = b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb'

    @patch('vanity_address.coins.bitcoin.sha256')
    def test_bytes_hashes_the_key_twice_with_sha26(self, sha256):
        sha256.return_value = self._first_hash

        bytes(self._private_key)

        sha256.assert_has_calls([
            call(self._private_key_with_prefix),
            call(self._first_hash),
        ])

    @patch('vanity_address.coins.bitcoin.base58encode')
    @patch('vanity_address.coins.bitcoin.sha256')
    def test_bytes_base58_encodes_the_private_key_with_the_correct_checksum(self, sha256, base58encode):
        sha256.return_value = self._second_hash
        base58encode.return_value = self._address

        bytes(self._private_key)

        base58encode.assert_called_once_with(self._private_key_with_checksum)

    @patch('vanity_address.coins.bitcoin.base58encode')
    def test_bytes_returns_the_base58encoded_result(self, base58encode):
        base58encode.return_value = self._address

        wif = bytes(self._private_key)

        self.assertEqual(wif, self._address)

    @patch('vanity_address.coins.bitcoin.sha256')
    def test_bytes_uses_the_correct_prefix_for_a_testnet_address(self, sha256):
        private_key = PrivateKey(12345, testnet=True)
        sha256.return_value = self._first_hash

        bytes(private_key)

        sha256.assert_any_call(self._testnet_private_key)

    @patch('vanity_address.coins.bitcoin.sha256')
    def test_bytes_adds_the_correct_suffix_for_a_compressed_address(self, sha256):
        private_key = PrivateKey(12345, compressed=True)
        sha256.return_value = self._first_hash

        bytes(private_key)

        sha256.assert_any_call(self._compressed_private_key)

    def test_is_testnet_key_returns_false_for_normal_keys(self):
        self.assertFalse(self._private_key.is_testnet_key())

    def test_is_testnet_key_returns_false_for_testnet_keys(self):
        private_key = PrivateKey(12345, testnet=True)

        self.assertTrue(private_key.is_testnet_key())

    def test_is_compressed_returns_false_for_normal_keys(self):
        self.assertFalse(self._private_key.is_compressed())

    def test_is_compressed_returns_false_for_compresseds(self):
        private_key = PrivateKey(12345, compressed=True)

        self.assertTrue(private_key.is_compressed())

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

    @patch('vanity_address.coins.bitcoin.hash160')
    def test_get_address_hashes_the_public_key_with_hash160(self, hash160):
        hash160.return_value = self._hash160_of_public_key

        self._public_key.get_address()

        hash160.assert_called_once_with(self._public_key_ecdsa)

    @patch('vanity_address.coins.bitcoin.hash256')
    @patch('vanity_address.coins.bitcoin.hash160')
    def test_get_address_hashes_the_ripemd_of_the_sha_of_the_public_key_with_hash256(self, hash160, hash256):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        self._public_key.get_address()

        hash256.assert_called_once_with(self._hash160_with_network_prefix)

    @patch('vanity_address.coins.bitcoin.base58encode')
    @patch('vanity_address.coins.bitcoin.hash256')
    @patch('vanity_address.coins.bitcoin.hash160')
    def test_get_address_base58encodes_the_ripemd_and_the_checksum(self, hash160, hash256, base58encode):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160

        self._public_key.get_address()

        base58encode.assert_called_once_with(self._hash160_with_checksum)

    @patch('vanity_address.coins.bitcoin.base58encode')
    def test_get_address_returns_the_base58encoded_address(self, base58encode):
        base58encode.return_value = self._address

        address = self._public_key.get_address()

        self.assertEqual(address, self._address)

    @patch('vanity_address.coins.bitcoin.hash256')
    @patch('vanity_address.coins.bitcoin.hash160')
    def test_get_address_prepends_the_correct_prefix_for_testnet_addresses(self, hash160, hash256):
        hash160.return_value = self._hash160_of_public_key
        hash256.return_value = self._hash256_of_hash160
        private_key = self._mock_private_key(12344, testnet=True)
        public_key = PublicKey(private_key)

        public_key.get_address()

        hash256.assert_called_once_with(self._hash160_with_testnet_prefix)

    @patch('vanity_address.coins.bitcoin.hash160')
    def test_get_address_prepends_the_correct_prefix_for_odd_compressed_keys(self, hash160):
        hash160.return_value = self._hash160_of_public_key
        private_key = self._mock_private_key(12345, compressed=True)
        public_key = PublicKey(private_key)

        public_key.get_address()

        hash160.assert_called_once_with(self._compressed_public_key_ecdsa_odd)

    @patch('vanity_address.coins.bitcoin.hash160')
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

