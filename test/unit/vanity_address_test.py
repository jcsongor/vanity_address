import re
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from bitcoin_vanity.vanity_address import Worker, CandidateGenerator, VanityAddress, VanityAddressGenerator
from test import Patcher


@patch('bitcoin_vanity.vanity_address.CandidateGenerator')
class VanityAddressGeneratorTest(TestCase, Patcher):
    def setUp(self):
        self._callback = MagicMock()
        self._callback.side_effect = [False, False, True, False, True]

    def test_generate_yields_the_matching_addresses(self, candidate_generator):
        expected_address1 = MagicMock()
        expected_address2 = MagicMock()
        candidate_generator.return_value.__enter__.return_value = iter([
            MagicMock(),
            MagicMock(),
            expected_address1,
            MagicMock(),
            expected_address2
        ])

        result1 = next(VanityAddressGenerator.generate(self._callback))
        result2 = next(VanityAddressGenerator.generate(self._callback))

        self.assertEqual(result1, expected_address1)
        self.assertEqual(result2, expected_address2)

    def test_generate_one_returns_the_first_matching_address(self, candidate_generator):
        expected_address = MagicMock()
        candidate_generator.return_value.__enter__.return_value = iter([
            MagicMock(),
            MagicMock(),
            expected_address,
        ])

        result = VanityAddressGenerator.generate_one(self._callback)

        self.assertEqual(result, expected_address)


class CandidateGeneratorTest(TestCase, Patcher):
    def setUp(self):
        self._event = self._patch('bitcoin_vanity.vanity_address.Event')
        self._queue = self._patch('bitcoin_vanity.vanity_address.Queue')
        self._process = self._patch('bitcoin_vanity.vanity_address.Process')
        self._worker = self._patch('bitcoin_vanity.vanity_address.Worker')

        self._generator = CandidateGenerator(2)

        self._results = [MagicMock(), MagicMock(), MagicMock()]
        self._queue.return_value.get.side_effect = self._results
        self._pattern = re.compile('.*match.*')

    def test_enter_creates_the_correct_number_of_processes(self):
        with self._generator as _:
            self._process.assert_has_calls([
                call(target=self._worker.return_value.run, args=(self._queue.return_value, self._event.return_value)),
                call(target=self._worker.return_value.run, args=(self._queue.return_value, self._event.return_value)),
            ], True)

    def test_enter_starts_the_correct_number_of_processes(self):
        with self._generator as _:
            self.assertEqual(self._process.return_value.start.call_count, 2)

    def test_next_fetches_results_from_the_queue(self):
        self._generate(3)

        self.assertEqual(self._queue.return_value.get.call_count, 3)

    def test_next_yields_results_from_the_queue(self):
        results = self._generate(3)

        self.assertEqual(self._results, results)

    def test_exit_sets_the_terminate_event(self):
        with self._generator as _:
            pass

        self._event.return_value.set.assert_called_once()

    def _generate(self, count):
        results = []
        with self._generator as generator:
            for _ in range(count):
                results.append(next(generator))
        return results


class WorkerTest(TestCase, Patcher):
    def setUp(self):
        self._rng = self._patch('bitcoin_vanity.vanity_address.SecretsRNG')
        self._private_key_generator = self._patch('bitcoin_vanity.vanity_address.PrivateKeyGenerator')
        self._public_key = self._patch('bitcoin_vanity.vanity_address.PublicKey')
        self._result_queue = MagicMock()

        self._terminate_event = MagicMock()
        self._terminate_event.is_set.side_effect = [False, False, False, True]

        self._worker = Worker()

    def test_init_initializes_private_key_generator(self):
        self._private_key_generator.assert_called_once_with(self._rng.return_value)

    def test_run_generates_private_keys_until_it_is_terminated(self):
        self._worker.run(self._result_queue, self._terminate_event)

        self.assertEqual(self._private_key_generator.return_value.generate_private_key.call_count, 3)

    def test_run_generates_public_keys_from_the_private_keys(self):
        private_keys = [MagicMock(), MagicMock(), MagicMock()]
        self._private_key_generator.return_value.generate_private_key.side_effect = private_keys

        self._worker.run(self._result_queue, self._terminate_event)

        self._public_key.assert_has_calls([call(private_key) for private_key in private_keys], True)

    def test_run_puts_generated_private_key_and_address_pairs_in_the_result_queue(self):
        private_keys = [MagicMock(), MagicMock(), MagicMock()]
        self._private_key_generator.return_value.generate_private_key.side_effect = private_keys
        addresses = ['abc001', 'abc002', 'abc002']
        self._public_key.return_value.get_address.side_effect = addresses

        self._worker.run(self._result_queue, self._terminate_event)

        self._result_queue.put.assert_has_calls(self._get_result_calls(private_keys, addresses))

    def _get_result_calls(self, private_keys, addresses):
        return [self._get_result_call(address, private_key) for private_key, address in zip(private_keys, addresses)]

    def _get_result_call(self, address, private_key):
        return call(VanityAddress(address=address, private_key=private_key))
