from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from bitcoin_vanity.private_key import PrivateKeyGenerator, SecretsRNG, PrivateKey


@patch('bitcoin_vanity.private_key.randbits')
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

    @patch('bitcoin_vanity.private_key.PrivateKey')
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

    def test_int_returns_the_private_key_as_an_integer(self):
        self.assertEqual(int(self._private_key), 12345)

    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_hashes_the_key_twice_with_sha26(self, sha256):
        sha256.return_value = self._first_hash

        bytes(self._private_key)

        sha256.assert_has_calls([
            call(self._private_key_with_prefix),
            call(self._first_hash),
        ])

    @patch('bitcoin_vanity.private_key.base58encode')
    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_base58_encodes_the_private_key_with_the_correct_checksum(self, sha256, base58encode):
        sha256.return_value = self._second_hash
        base58encode.return_value = self._address

        bytes(self._private_key)

        base58encode.assert_called_once_with(self._private_key_with_checksum)

    @patch('bitcoin_vanity.private_key.base58encode')
    def test_bytes_returns_the_base58encoded_result(self, base58encode):
        base58encode.return_value = self._address

        wif = bytes(self._private_key)

        self.assertEqual(wif, self._address)

    def test_bytes_returns_the_private_key_in_wif_format(self):
        wif = bytes(self._private_key)

        self.assertEqual(wif, self._address)

    def test_str_returns_the_private_key_in_wif_format(self):
        wif = str(self._private_key)

        self.assertEqual(wif, self._address.decode('utf-8'))

    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_uses_the_correct_prefix_for_a_testnet_address(self, sha256):
        private_key = PrivateKey(12345, testnet=True)
        sha256.return_value = self._first_hash

        bytes(private_key)

        sha256.assert_any_call(self._testnet_private_key)

    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_adds_the_correct_suffix_for_a_compressed_address(self, sha256):
        private_key = PrivateKey(12345, compressed=True)
        sha256.return_value = self._first_hash

        bytes(private_key)

        sha256.assert_any_call(self._compressed_private_key)
