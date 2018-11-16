from unittest import TestCase

from bitcoin_vanity.lib.hash import hash256, ripemd160


class Hash256Test(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._hash256_result = 'd24dbe11526b088edded1aee68c5ea2aa175bee0cc0e695f3d188f14607ef5c5'

    def test_hash256_returns_the_correct_hash(self):
        result = hash256(self._hex_str)

        self.assertEqual(result, self._hash256_result)

class Hash160Test(TestCase):
    def setUp(self):
        self._hex_str = '1A2B3C'
        self._ripemd160_result = '2885f0092763dc3b0761e43cb64a9de1af9a16bb'

    def test_ripemd160_returns_the_correct_hash(self):
        result = ripemd160(self._hex_str)

        self.assertEqual(result, self._ripemd160_result)
