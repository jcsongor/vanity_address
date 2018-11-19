import re
from unittest import TestCase
from unittest.mock import MagicMock, call

from bitcoin_vanity.vanity_address import Worker, Generator, CandidateGenerator
from test import Patcher


class GeneratorTest(TestCase, Patcher):
    def setUp(self):
        self._candidate_generator = self._patch('bitcoin_vanity.vanity_address.CandidateGenerator')
        self._event = self._patch('bitcoin_vanity.vanity_address.Event')
        self._queue = self._patch('bitcoin_vanity.vanity_address.Queue')
        self._process = self._patch('bitcoin_vanity.vanity_address.Process')
        self._worker = self._patch('bitcoin_vanity.vanity_address.Worker')

        self._generator = Generator()

        self._queue.return_value.get.side_effect = [
            ('key1', 'something'),
            ('key2', 'something'),
            ('key3', 'match1'),
            ('key4', 'match2'),
            ('key5', 'something'),
            ('key6', 'match3'),
            ('key7', 'something'),
            ('key8', 'match4'),
        ]
        self._pattern = re.compile('.*match.*')

    def test_init_initializes_candidate_generator(self):
        self._candidate_generator.assert_called_once()

    def test_init_initializes_worker(self):
        self._worker.assert_called_once_with(self._candidate_generator.return_value)

    def test_generate_creates_the_correct_number_of_processes(self):
        self._generator.generate(self._pattern, 1, 4)

        self._process.assert_has_calls([
            call(target=self._worker.return_value.run, args=(self._queue.return_value, self._event.return_value)),
            call(target=self._worker.return_value.run, args=(self._queue.return_value, self._event.return_value)),
            call(target=self._worker.return_value.run, args=(self._queue.return_value, self._event.return_value)),
            call(target=self._worker.return_value.run, args=(self._queue.return_value, self._event.return_value)),
        ], True)

    def test_generate_starts_the_correct_number_of_processes(self):
        self._generator.generate(self._pattern, 1, 4)

        self.assertEqual(self._process.return_value.start.call_count, 4)

    def test_generate_polls_the_queue_until_it_collects_the_correct_number_of_addresses(self):
        self._generator.generate(self._pattern, 3, 3)

        self.assertEqual(self._queue.return_value.get.call_count, 6)

    def test_generate_returns_the_correct_number_of_addresses(self):
        addresses = self._generator.generate(self._pattern, 3, 3)

        self.assertEqual(addresses, [
            ('key3', 'match1'),
            ('key4', 'match2'),
            ('key6', 'match3'),
        ])

    def test_generate_sets_the_terminate_event(self):
        self._generator.generate(self._pattern, 3, 3)

        self._event.return_value.set.assert_called_once()


class WorkerTest(TestCase):
    def setUp(self):
        self._candidate_generator = MagicMock()
        self._result_queue = MagicMock()

        self._terminate_event = MagicMock()
        self._terminate_event.is_set.side_effect = [False, False, False, True]

        self._worker = Worker(self._candidate_generator)

    def test_run_generates_candidates_until_it_is_terminated(self):
        self._worker.run(self._result_queue, self._terminate_event)

        self.assertEqual(self._candidate_generator.generate_candidate.call_count, 3)

    def test_run_puts_generated_candidates_in_the_result_queue(self):
        candidates = [MagicMock(), MagicMock(), MagicMock()]
        self._candidate_generator.generate_candidate.side_effect = candidates

        self._worker.run(self._result_queue, self._terminate_event)

        self._result_queue.put.assert_has_calls([call(candidate) for candidate in candidates])


class CandidateGeneratorTest(TestCase, Patcher):
    def setUp(self):
        self._rng = self._patch('bitcoin_vanity.vanity_address.SecretsRNG')
        self._private_key_generator = self._patch('bitcoin_vanity.vanity_address.PrivateKeyGenerator')
        self._public_key = self._patch('bitcoin_vanity.vanity_address.PublicKey')
        self._candidate_generator = CandidateGenerator()

    def test_init_initializes_private_key_generator(self):
        self._private_key_generator.assert_called_once_with(self._rng.return_value)

    def test_generate_candidate_generates_private_key(self):
        self._candidate_generator.generate_candidate()

        self._private_key_generator.return_value.generate_private_key.assert_called_once()

    def test_generate_candidate_generates_public_key(self):
        self._private_key_generator.return_value.generate_private_key.return_value = 12345

        self._candidate_generator.generate_candidate()

        self._public_key.assert_called_once_with(12345)
