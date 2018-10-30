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
        self._rng.randbits.side_effect = [
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140,
        ]

        self._private_key_generator = PrivateKeyGenerator(self._rng)

    def test_generate_private_key_generates_256_bit_integers_until_it_finds_a_valid_key(self):
        self._private_key_generator.generate_private_key()

        self._rng.randbits.assert_has_calls([call(256), call(256), call(256)])

    def test_generate_private_key_returns_the_first_valid_key_it_finds(self):
        private_key = self._private_key_generator.generate_private_key()

        self.assertEqual(private_key, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140),

class PrivateKeyTest(TestCase):
    def setUp(self):
        self._private_key = PrivateKey(12345)
    def test_int_returns_the_private_key_as_an_integer(self):
        self.assertEqual(int(self._private_key), 12345)

    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_hashes_the_key_twice_with_sha26(self, sha256):
        sha256.return_value.hexdigest.return_value = '5976C6B48D1DC862AEB0C8BC3126A2751CC48E36737009DF688A9F0787A4624A'

        bytes(self._private_key)

        sha256.assert_has_calls([
            call(b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0009'),
            call(b'Yv\xc6\xb4\x8d\x1d\xc8b\xae\xb0\xc8\xbc1&\xa2u\x1c\xc4\x8e6sp\t\xdfh\x8a\x9f\x07\x87\xa4bJ'),
        ], True)

    @patch('bitcoin_vanity.private_key.b58encode')
    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_base58_encodes_the_private_key_with_the_correct_checksum(self, sha256, b58encode):
        sha256.return_value.hexdigest.return_value = '180D8C2E6CBBFFCE35A0BB172CBAC966FD9AC8B7F5CB9D70C3DC8C70B90AC88C'
        b58encode.return_value = b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb'

        bytes(self._private_key)

        b58encode.assert_called_once_with(b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0009\x18\r\x8c.')

    @patch('bitcoin_vanity.private_key.b58encode')
    def test_bytes_returns_the_b58encoded_result(self,b58encode):
        b58encode.return_value = b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb'

        wif = bytes(self._private_key)

        self.assertEqual(wif, b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb')

    def test_bytes_returns_the_private_key_in_wif_format(self):
        wif = bytes(self._private_key)

        self.assertEqual(wif, b'5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb')

    def test_str_returns_the_private_key_in_wif_format(self):
        wif = str(self._private_key)

        self.assertEqual(wif, '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEss4BPiFsjb')

    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_uses_the_correct_prefix_for_a_testnet_address(self, sha256):
        private_key = PrivateKey(12345, testnet=True)
        sha256.return_value.hexdigest.return_value = '5976C6B48D1DC862AEB0C8BC3126A2751CC48E36737009DF688A9F0787A4624A'

        bytes(private_key)

        sha256.assert_has_calls([
            call(b'\xef\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0009'),
        ], True)

    @patch('bitcoin_vanity.private_key.sha256')
    def test_bytes_adds_the_correct_suffix_for_a_compressed_address(self, sha256):
        private_key = PrivateKey(12345, compressed=True)
        sha256.return_value.hexdigest.return_value = '5976C6B48D1DC862AEB0C8BC3126A2751CC48E36737009DF688A9F0787A4624A'

        bytes(private_key)

        sha256.assert_has_calls([
            call(b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0009\x01'),
        ], True)
