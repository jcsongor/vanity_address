from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from bitcoin_vanity.private_key import PrivateKeyGenerator, SecretsRNG


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

