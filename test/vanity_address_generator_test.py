from unittest import TestCase
from unittest.mock import patch, MagicMock, call

from bitcoin_vanity.vanity_address_generator import VanityAddressGenerator


@patch('bitcoin_vanity.vanity_address_generator.PublicKey')
@patch('bitcoin_vanity.vanity_address_generator.PrivateKeyGenerator.generate_private_key')
class VanityAddressGeneratorTest(TestCase):
    def setUp(self):
        self._vanity_address_generator = VanityAddressGenerator()
        self._pattern = MagicMock()
        self._pattern.match.side_effect = [None, None, True]
        self._private_keys = ['private_key1', 'private_key2', 'private_key3']
        self._addresses = ['address1', 'address2', 'address3']

    def test_generate_matching_address_generates_private_keys_until_it_finds_a_matching_one(self, generate_private_key, _):
        self._vanity_address_generator.generate_matching_address(self._pattern)

        self.assertEqual(generate_private_key.call_count, 3)

    def test_generate_matching_address_generates_public_keys_until_it_finds_a_matching_one(self, generate_private_key, public_key):
        generate_private_key.side_effect = self._private_keys

        self._vanity_address_generator.generate_matching_address(self._pattern)

        public_key.assert_has_calls([call('private_key1'), call('private_key2'), call('private_key3')], True)

    def test_generate_matching_address_gets_the_addresses_of_the_public_keys(self, generate_private_key, public_key):
        generate_private_key.side_effect = self._private_keys

        self._vanity_address_generator.generate_matching_address(self._pattern)

        self.assertEqual(public_key.return_value.get_address.call_count, 3)

    def test_generate_matching_address_tries_to_match_the_pattern_with_the_addresses(self, generate_private_key, public_key):
        generate_private_key.side_effect = self._private_keys
        public_key.return_value.get_address.side_effect = self._addresses

        self._vanity_address_generator.generate_matching_address(self._pattern)

        self._pattern.match.assert_has_calls([call('address1'), call('address2'), call('address3')])

    def test_generate_matching_address_returns_the_first_matching_address(self, generate_private_key, public_key):
        generate_private_key.side_effect = self._private_keys
        public_key.return_value.get_address.side_effect = self._addresses

        address = self._vanity_address_generator.generate_matching_address(self._pattern)

        self.assertEqual(address, 'address3')
