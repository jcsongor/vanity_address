from unittest import TestCase
from unittest.mock import patch
from bitcoin_vanity.private_key import SecretsRNG


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
