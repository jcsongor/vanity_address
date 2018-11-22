from collections import namedtuple
from multiprocessing import Event, Process, Queue
from typing import Callable, Generator
from bitcoin_vanity.private_key import PrivateKey, PrivateKeyGenerator, SecretsRNG
from bitcoin_vanity.public_key import PublicKey

VanityAddress = namedtuple('VanityAddress', ['address', 'private_key'])

class VanityAddressGenerator:
    @staticmethod
    def generate(callback: Callable[[bytes], bool]) -> Generator[VanityAddress, None, None]:
        with CandidateGenerator() as addresses:
            for vanity_address in addresses:
                if callback(vanity_address.address):
                    yield vanity_address

    @staticmethod
    def generate_one(callback: Callable[[bytes], bool]) -> (bytes, PrivateKey):
        with CandidateGenerator() as addresses:
            for vanity_address in addresses:
                if callback(vanity_address.address):
                    return vanity_address



class CandidateGenerator:
    def __init__(self, worker_count: int = 4):
        self._result_queue = Queue()
        self._terminate_event = Event()
        self._worker = Worker()
        self._worker_count = worker_count

    def __enter__(self) -> Generator[VanityAddress, None, None]:
        self._start_workers(self._worker_count)
        return self._generate()

    def __exit__(self, *args, **kwargs):
        self._terminate_event.set()

    def _generate(self) -> Generator[VanityAddress, None, None]:
        while True:
            yield self._result_queue.get()

    def _start_workers(self, worker_count) -> None:
        for _ in range(worker_count):
            self._start_worker()

    def _start_worker(self) -> None:
        Process(target=self._worker.run, args=(self._result_queue, self._terminate_event)).start()


class Worker:
    def __init__(self):
        rng = SecretsRNG()
        self._private_key_generator = PrivateKeyGenerator(rng)

    def run(self, result_queue: Queue, terminate_event: Event) -> None:
        while not terminate_event.is_set():
            result_queue.put(self._generate_candidate())

    def _generate_candidate(self) -> VanityAddress:
        private_key = self._private_key_generator.generate_private_key()
        public_key = PublicKey(private_key)
        return VanityAddress(public_key.get_address(), private_key)
