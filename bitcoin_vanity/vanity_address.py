from multiprocessing import Queue, Event, Process
from re import Pattern
from bitcoin_vanity.private_key import PrivateKeyGenerator, SecretsRNG, PrivateKey
from bitcoin_vanity.public_key import PublicKey


class Generator:
    def __init__(self):
        self._result_queue = Queue()
        self._terminate_event = Event()
        self._worker = Worker(CandidateGenerator())

    def generate(self, pattern: Pattern, address_count: int = 1, worker_count: int = 4) -> list((PrivateKey, str)):
        self._start_workers(worker_count)

        addresses = self._collect_results(address_count, pattern)

        self._terminate_event.set()

        return addresses

    def _collect_results(self, address_count, pattern):
        addresses = []
        while len(addresses) < address_count:
            private_key, address = self._result_queue.get()
            if pattern.match(address) is not None:
                addresses.append((private_key, address))
        return addresses

    def _start_workers(self, worker_count):
        for _ in range(worker_count):
            self._start_worker()

    def _start_worker(self):
        Process(target=self._worker.run, args=(self._result_queue, self._terminate_event)).start()


class CandidateGenerator:
    def __init__(self):
        rng = SecretsRNG()
        self._private_key_generator = PrivateKeyGenerator(rng)

    def generate_candidate(self) -> (PrivateKey, str):
        private_key = self._private_key_generator.generate_private_key()
        public_key = PublicKey(private_key)
        return private_key, str(public_key.get_address())


class Worker:
    def __init__(self, candidate_generator: CandidateGenerator):
        self._candidate_generator = candidate_generator

    def run(self, result_queue: Queue, terminate_event: Event):
        while not terminate_event.is_set():
            result_queue.put(self._candidate_generator.generate_candidate())
